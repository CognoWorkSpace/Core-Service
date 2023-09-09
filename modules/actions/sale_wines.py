from typing import List, Tuple
from .chat import ChatBase
from utils.logging import LOGGER
from langchain.agents import Tool, tool
from langchain.prompts import StringPromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ChatMessageHistory
import const

from modules.factories.model_factory import create_model

from flask import current_app
from langchain import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import messages_to_dict
from langchain.agents import Tool
from databaseMod.milvusDB import MilvusDB

from modules.prompts.seller_template import seller_with_database_template_products, \
    seller_with_agent_memory_template_products_tools_chat_history_agent_scratchpad_input
from modules.prompts.memory_template import memory_template_chat_history_input

mvs_db = MilvusDB()
mvs_db.db_name = 'wine'
mvs_db.collection = 'wine_data'
output_fields = [field.name for field in mvs_db.collection.schema.fields if
                 field.name not in {'id', 'wine_info_embed'}]
chat_history = ChatMessageHistory()  # TODO: Change the memory location to save all message from users


class SalesWinesAction(ChatBase):
    def __init__(self, model=None, in_memory=True, chats_history=None, number=10):
        super().__init__(model, in_memory, chats_history, number)

    def search_from_cache(self):
        pass

    def set_up_tools(self):
        tools = [
            Tool.from_function(
                name="wine search tool",
                description="A wine search tool, use it when you need to search products from your company",
                func=self.database_search,
                return_direct=True
            )
        ]
        tools = []
        return tools

    def database_search(self, query):

        LOGGER.info("get into the database_search, query:{}".format(query))
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

    def chat_with_database(self, query):
        LOGGER.info("get into the chat_with_database, query:{}".format(query))
        template = seller_with_database_template_products
        LOGGER.info("get into the chat_with_database2, query:{}".format(query))
        products = self.database_search(query)

        LOGGER.info("Database result: {}".format(products))
        prompt = PromptTemplate(
            input_variables=["products"],
            template=template,
        )
        template = prompt.format(products=products) + memory_template_chat_history_input
        LOGGER.info("Prompt is: {}".format(template))
        memory = ConversationBufferWindowMemory(
            k=current_app.config.get("OPENAI_BUFFER_TOP_K", 5), chat_memory=chat_history, ai_prefix="CognoPal",
            human_prefix="Customer",
            memory_key="chat_history",
            input_key="input")

        prompt = PromptTemplate(input_variables=["chat_history", "input"], template=template)

        conversation = ConversationChain(
            llm=create_model(current_app.config.get("MODEL", const.OPENAI)), verbose=True, memory=memory, prompt=prompt
        )

        reply = conversation.predict(input=query)
        LOGGER.info("Reply generated: {}".format(reply))
        history = messages_to_dict(chat_history.messages)
        LOGGER.info("Chat function ends.")

        return {"reply": reply, "history": history}

    def chat_response(self, query):
        LOGGER.info("get into the chat_response")
        prompt = CustomPromptTemplate(
            template=seller_with_agent_memory_template_products_tools_chat_history_agent_scratchpad_input,
            tools=self.set_up_tools(),
            input_variables=["input", "intermediate_steps", "chat_history", "products"]
        )
        LOGGER.info("The prompt is: {}".format(prompt))
        response = self.chat(query, prompt=prompt)
        return response


class CustomPromptTemplate(StringPromptTemplate):
    template: str
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)
