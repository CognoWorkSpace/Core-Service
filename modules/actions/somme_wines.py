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
from modules.prompts.sommelier_template import sommelier_template_input_history



class SommeAction(ChatBase):
    def __init__(self, model=None, in_memory=True, chat_history_dict=None, number=10):
        super().__init__(model, in_memory, chat_history_dict, number)

    def search_from_cache(self):
        pass

    def chat(self, query):
        """Searches the API for the query."""
        chat_history = ChatMessageHistory()
        LOGGER.info("get into the chat_response")
        prompt = PromptTemplate(
            template=sommelier_template_input_history,
            input_variables=["input", "history"]
        )
        LOGGER.info("The prompt is: {}".format(prompt))
        conversation = ConversationChain(
            prompt=prompt,
            llm=create_model(model_name=current_app.config.get("MODEL", const.OPENAI)),
            verbose=True,
            memory=ConversationBufferWindowMemory(k=5, chat_memory=chat_history),
        )
        reply = conversation.predict(input=query)
        LOGGER.info("return response is {}".format(reply))
        history = messages_to_dict(chat_history.messages)
        return {"reply": reply, "history": history}

    def chat_given_history(self, query):
        """Searches the API for the query."""
          # Change the memory location to save all message from users
        chat_history_local = ChatMessageHistory()
        LOGGER.info('Get HISTORY{}'.format(self.chat_history_dict))
        messages = messages_from_dict(self.chat_history_dict)
        # Add every message to history Object
        for message in messages:
            chat_history_local.add_message(message=message)
        LOGGER.info("get into the chat_response")
        prompt = PromptTemplate(
            template=sommelier_template_input_history,
            input_variables=["input", "history"]
        )
        LOGGER.info("The prompt is: {}".format(prompt))
        conversation = ConversationChain(
            prompt=prompt,
            llm=create_model(model_name=current_app.config.get("MODEL", const.OPENAI)),
            verbose=True,
            memory=ConversationBufferWindowMemory(k=5, chat_memory=chat_history_local),
        )
        reply = conversation.predict(input=query)
        LOGGER.info("return response is {}".format(reply))
        history = messages_to_dict(chat_history_local.messages)
        return {"reply": reply, "history": history}