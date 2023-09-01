from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import messages_from_dict, messages_to_dict
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser, Agent
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re
import const
from flask import current_app
from modules.factories.model_factory import create_model

from utils.logging import LOGGER

# TODO: try to connect to MYSQL to acquire history message based on database. The test implementation is let all the user share one common history message.
chat_history = ChatMessageHistory()  # Change the memory location to save all message from users


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

    def chat(self, query, prompt=""):
        tools = self.set_up_tools()
        LOGGER.info("get into chat")
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
            # Convert dicts to message object
            self.convert_message(history)
            # Create memory object that only keep 5 closest messages
            memory = self.keep_memory_message(num, with_memory)

            # Create a Conversation Chain
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

                memory = ConversationBufferWindowMemory(k=5, chat_memory=chat_history, memory_key="chat_history", input_key="input")

                output_parser = CustomOutputParser()

                conversation = LLMChain(
                    llm=create_model(model_name),
                    verbose=True,
                    prompt=prompt,
                )
                tool_names = [tool.name for tool in tools]
                agent = LLMSingleActionAgent(
                    llm_chain=conversation,
                    output_parser=output_parser,
                    stop=["\nObservation:"],
                    allowed_tools=tool_names,
                )
                agent_executor = AgentExecutor.from_agent_and_tools(
                    agent=agent, tools=tools, verbose=True, memory=memory
                )

                reply = agent_executor.run({'input': query, 'salesperson_name': 'Dijkstra', 'company_name': 'Test company_name'})
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

    def search_from_knowledge_base(self):
        pass

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