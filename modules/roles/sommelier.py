from modules.actions.somme_wines import SommeAction
from utils.logging import LOGGER


class Sommelier:
    def __init__(self, query=None, model=None, in_memory=None,chat_history_dict=None, number=10):
        self.query = query
        self.model = model
        self.memory = in_memory
        self.chat_history_dict = chat_history_dict
        self.num = number

    def chat_reply(self):
    # handle the return data to logic service
        LOGGER.info("get into the chat_reply")
        chat_reply = SommeAction(model=self.model, in_memory=self.memory, chat_history_dict=self.chat_history_dict, number=self.num).chat(query=self.query)
        return chat_reply

    def chat_reply_given_history(self):
        LOGGER.info("get into the chat_reply_given_history")
        chat_reply = SommeAction(model=self.model, in_memory=self.memory, chat_history_dict=self.chat_history_dict, number=self.num).chat(query=self.query)
        chat_reply = SommeAction(model=self.model, in_memory=self.memory, chat_history_dict=self.chat_history_dict,
                                      number=self.num).chat_given_history(
            query=self.query)
        return chat_reply

    def get_history(self):
        return SommeAction().get_history()
