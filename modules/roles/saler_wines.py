from modules.actions.sale_wines import SalesWinesAction
from utils.logging import LOGGER


class SalesWines:
    def __init__(self, query=None, model=None, in_memory=None, chat_history_dict=None, username="default",  number=10):
        self.query = query
        self.model = model
        self.memory = in_memory
        self.chat_history_dict = chat_history_dict
        self.num = number
        self.username = username

    def chat_reply(self):
    # handle the return data to logic service
        LOGGER.info("get into the chat_reply, query:{}".format(self.query))
        chat_reply = SalesWinesAction(model=self.model, in_memory=self.memory, chat_history_dict=self.chat_history_dict, number=self.num, username=self.username).chat_with_database(query=self.query)
        return chat_reply

    def chat_reply_given_history(self):
        LOGGER.info("get into the chat_reply, query:{}".format(self.query))
        chat_reply = SalesWinesAction(model=self.model, in_memory=self.memory, chat_history_dict=self.chat_history_dict,
                                      number=self.num, username=self.username).chat_with_database_given_history(query=self.query)
        return chat_reply
    def get_history(self):
        return SalesWinesAction().get_history()
