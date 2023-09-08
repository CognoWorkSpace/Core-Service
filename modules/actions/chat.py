from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import messages_from_dict, messages_to_dict
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser, Agent
from langchain.chains import ConversationalRetrievalChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re
import const

from databaseMod.milvusDB import MilvusDB
from flask import current_app
from modules.factories.connection_string_factory import create_connection_string
from modules.factories.database_factory import create_database
from modules.factories.embedding_factory import create_embedding
from modules.factories.model_factory import create_model

from utils.logging import LOGGER

# TODO: try to connect to MYSQL to acquire history message based on database. The test implementation is let all the user share one common history message.
chat_history = ChatMessageHistory()  # Change the memory location to save all message from users

mvs_db = MilvusDB()
mvs_db.db_name = 'wine'
mvs_db.collection = 'wine_data'
output_fields = [field.name for field in mvs_db.collection.schema.fields if
                 field.name not in {'id', 'wine_info_embed'}]
def wine_search(query: str) -> str:
    """A wine search tool, use it when you need to search products from your company"""

    res = mvs_db.conduct_vector_similar_search(query=query, limit=5,
                                               output_fields=output_fields)

    entity_strings = []
    index = 1
    for search_res in res:
        for hit in search_res:
            entity = hit.entity.to_dict()["entity"]
            entity_str = "* Product " + str(index) + ": " + ', '.join(
                f"{key}: {value}" for key, value in entity.items())
            entity_strings.append(entity_str)
            index = index + 1

    result_str = '\n'.join(entity_strings)
    LOGGER.info("Search Tool found:{}".format(result_str))
    return result_str

class ChatBase:
    def __init__(self, model=None, in_memory=None, chats_history=None, number=None):
        self.model_name = model
        self.with_memory = in_memory
        self.history = chats_history
        self.num = number

    def convert_message(self, history):
        try:
            messages = messages_from_dict(history)
        except Exception as e:
            LOGGER.error("User provided an invalid chat history: {}".format(e))
            raise ValueError("Please check the format of history message you post: {}".format(e))
            # Add every message to history Object
        for message in messages:
            chat_history.add_message(message=message)
        LOGGER.info("Chat history converted.")

    def keep_memory_message(self, num, with_memory):
        memory = ConversationBufferWindowMemory(
            k=current_app.config.get("OPENAI_BUFFER_TOP_K", num) if with_memory else 0, chat_memory=chat_history, memory_key="chat_history", input_key="input")
        LOGGER.info("Memory object created.")
        return memory

    def chat(self, query, prompt="", isSearch=False):
        tools = self.set_up_tools()
        LOGGER.info("get into chat func")
        global model_name, with_memory, history, conversation, num
        if self.model_name is None:
            model_name = current_app.config.get("MODEL", const.OPENAI)
        if self.with_memory is None:
            with_memory = False
        else:
            with_memory = self.with_memory
        if self.history is None:
            history = []
        else:
            history = self.history
        if self.num is None:
            num = 5
        else:
            num = self.num
        # LOGGER.info(model_name, with_memory, history, num)
        LOGGER.info(
            "Chat function starts with query: {}, model_name: {}, with_memory: {}, history length: {}.".format(query,
                                                                                                               model_name,
                                                                                                               with_memory,
                                                                                                               len(history)))
        try:
            # if isSearch is True:
            #     response = self.search_from_knowledge_base(query=query)
            #     LOGGER.info("DataBase result{}".format(response['reply']))
            #     return response
            # Create a Conversation Chain
            # Convert dicts to message object
            self.convert_message(history)
            # Create memory object that only keep 5 closest messages
            memory = self.keep_memory_message(num, with_memory)
            if prompt is None and len(tools) == 0:
                conversation = ConversationChain(
                    llm=create_model(model_name),
                    verbose=True,
                    memory=memory,
                )
                LOGGER.info("Conversation Chain created.")

                # Get the reply(string) from the conversation Chain
                reply = conversation.predict(input=query)

                LOGGER.info("Reply generated: {}".format(reply))

                history = messages_to_dict(chat_history.messages)

                LOGGER.info("Chat function ends.")

                return {"reply": reply, "history": history}
            else:

                products = wine_search(query)
                memory = ConversationBufferWindowMemory(k=5, chat_memory=chat_history, memory_key="chat_history", input_key="input")

                output_parser = CustomOutputParser()

                conversation = LLMChain(
                    llm=create_model(model_name),
                    verbose=True,
                    prompt=prompt,
                )
                tool_names = [tool.name for tool in tools]
                LOGGER.info("Tools name:{}".format(tool_names))
                agent = LLMSingleActionAgent(
                    llm_chain=conversation,
                    output_parser=output_parser,
                    stop=["\nObservation:"],
                    allowed_tools=tool_names,
                )
                agent_executor = AgentExecutor.from_agent_and_tools(
                    agent=agent, tools=tools, verbose=True, memory=memory
                )

                reply = agent_executor.run({'input': query, 'products': products})
                LOGGER.info("Reply generated: {}".format(reply))


                history = messages_to_dict(chat_history.messages)
                LOGGER.info("Chat function ends.")

                return {"reply": reply, "history": history}
        except ValueError as e:
            raise ValueError(e)
        except Exception as e:
            LOGGER.error("An unexpected error occurred in chat function: {}".format(e))
            raise Exception(e)

    def get_history(self):
        return messages_to_dict(chat_history.messages)

    def search_from_knowledge_base(self, query):

        LOGGER.info("Start Searching")
        # Creating Database connection string
        connection_string = create_connection_string(database_name=current_app.config.get("DATABASE", const.MILVUS))
        # Creating embedding method
        embeddings = create_embedding()
        # Creating Database
        database = create_database(database_name=current_app.config.get("DATABASE", const.MILVUS),
                                   collection_name='wine_data',
                                   connection_string=connection_string, embeddings=embeddings)

        memory = ConversationBufferWindowMemory(
            memory_key="chat_history", k=10, chat_memory=chat_history,
            return_messages=True)
        docs = database.similarity_search(query)
        LOGGER.info("DataBase Result{}".format(docs))
        qa = ConversationalRetrievalChain.from_llm(
            llm=create_model(model_name),
            retriever=database.as_retriever(search_kwargs={"k": 5}), memory=memory)
        reply = qa({"question": query})
        history = messages_to_dict(chat_history.messages)
        return {"reply": reply["answer"], "history": history}

    def search_from_cache(self):
        pass

    def set_up_tools(self):
        tools = []
        return tools


class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise OutputParserException(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)