from typing import List, Tuple
from .chat import ChatBase
from utils.logging import LOGGER
from langchain.agents import Tool, tool
from langchain.prompts import StringPromptTemplate
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser, Agent
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ChatMessageHistory
from langchain.schema import messages_from_dict, messages_to_dict
from utils.chat_history import get_or_create_chat_history
import const

from modules.factories.model_factory import create_model

from flask import current_app
from langchain import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import messages_to_dict
from langchain.agents import Tool

from modules.prompts.seller_template import seller_with_database_template_products, \
    seller_with_agent_memory_template_products_tools_chat_history_agent_scratchpad_input
from modules.prompts.memory_template import memory_template_chat_history_input

from utils.database import mvs_db_wines, output_fields_wines


class SalesWinesAction(ChatBase):
    def __init__(self, model=None, in_memory=True, chat_history_dict=None, number=10, username=""):
        super().__init__(model, in_memory, chat_history_dict, number, username)

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
        res = mvs_db_wines.conduct_vector_similar_search(query=query, limit=5,
                                                   output_fields=output_fields_wines)

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

    def chat_with_database_given_history (self, query):

        # This is the local chat_history, created based on API history
        chat_history_local = ChatMessageHistory()
        LOGGER.info('Get HISTORY{}'.format(self.chat_history_dict))
        messages = messages_from_dict(self.chat_history_dict)
        # Add every message to history Object
        for message in messages:
            chat_history_local.add_message(message=message)

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
            k=current_app.config.get("OPENAI_BUFFER_TOP_K", 5), chat_memory=chat_history_local,
            ai_prefix="CognoPal",
            human_prefix="Customer",
            memory_key="chat_history",
            input_key="input")

        prompt = PromptTemplate(input_variables=["chat_history", "input"], template=template)

        conversation = ConversationChain(
            llm=create_model(current_app.config.get("MODEL", const.OPENAI)), verbose=True, memory=memory, prompt=prompt
        )

        reply = conversation.predict(input=query)
        LOGGER.info("Reply generated: {}".format(reply))
        history = messages_to_dict(chat_history_local.messages)
        LOGGER.info("Chat function ends.")

        return {"reply": reply, "history": history}
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
            k=current_app.config.get("OPENAI_BUFFER_TOP_K", 5), chat_memory=get_or_create_chat_history(self.username), ai_prefix="CognoPal",
            human_prefix="Customer",
            memory_key="chat_history",
            input_key="input")

        prompt = PromptTemplate(input_variables=["chat_history", "input"], template=template)

        conversation = ConversationChain(
            llm=create_model(current_app.config.get("MODEL", const.OPENAI)), verbose=True, memory=memory, prompt=prompt
        )

        reply = conversation.predict(input=query)
        LOGGER.info("Reply generated: {}".format(reply))
        history = messages_to_dict(get_or_create_chat_history(self.username).messages)
        LOGGER.info("Chat function ends.")

        return {"reply": reply, "history": history}

    def chat_with_agent(self, query):
        template = seller_with_agent_memory_template_products_tools_chat_history_agent_scratchpad_input
        products = self.database_search(query)
        prompt = CustomPromptTemplate(
            template=template,
            tools=self.set_up_tools(),
            input_variables=["input", "intermediate_steps", "chat_history", "products"]
        )
        tools = self.set_up_tools()
        memory = ConversationBufferWindowMemory(
            k=current_app.config.get("OPENAI_BUFFER_TOP_K", 5), chat_memory=get_or_create_chat_history(self.username),
            memory_key="chat_history",
            input_key="input")
        output_parser = self.CustomOutputParser()
        conversation = LLMChain(
            llm=create_model(current_app.config.get("MODEL", const.OPENAI)),
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
        history = messages_to_dict(get_or_create_chat_history(self.username).messages)
        LOGGER.info("Chat function ends.")
        return {"reply": reply, "history": history}


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
