from typing import List, Tuple
from .chat import ChatBase
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ChatMessageHistory
import const
from flask import current_app
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from utils.logging import LOGGER
from langchain.schema import messages_from_dict, messages_to_dict
from modules.factories.model_factory import create_model

from modules.prompts.informer_template import informer_template_info
from modules.prompts.memory_template import memory_template_chat_history_input

from llama_index import GPTVectorStoreIndex
from llama_index import SimpleDirectoryReader


class InformAction(ChatBase):
    def __init__(self, model=None, in_memory=True, chat_history_dict=None, number=10):
        super().__init__(model, in_memory, chat_history_dict, number)

    def search_from_cache(self):
        pass

    def doc_search(self, query):
        documents = SimpleDirectoryReader('./src').load_data()
        index = GPTVectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        return response

    def chat_given_history(self, query):
        pass

    def chat_with_pdf(self, query):
        # This is the local chat_history, created based on API history
        chat_history_local = ChatMessageHistory()

        template = informer_template_info
        info = self.doc_search(query)

        LOGGER.info("Search result: {}".format(info))
        prompt = PromptTemplate(
            input_variables=["info"],
            template=template,
        )
        template = prompt.format(info=info) + memory_template_chat_history_input
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
    def chat_with_pdf_given_history(self, query):
        # This is the local chat_history, created based on API history
        chat_history_local = ChatMessageHistory()
        LOGGER.info('Get HISTORY{}'.format(self.chat_history_dict))
        messages = messages_from_dict(self.chat_history_dict)
        # Add every message to history Object
        for message in messages:
            chat_history_local.add_message(message=message)

        # Load company's info from PDF
        info = self.doc_search(query)

        template = informer_template_info
        info = self.doc_search(query)

        LOGGER.info("Search result: {}".format(info))
        prompt = PromptTemplate(
            input_variables=["info"],
            template=template,
        )
        template = prompt.format(info=info) + memory_template_chat_history_input
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
