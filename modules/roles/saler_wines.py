from modules.actions.sale_wines import SalesWinesAction
from utils.logging import LOGGER


class SalesWines:
    def __init__(self, query=None, model=None, in_memory=None, chats_history=None, username="default",  number=10):
        self.query = query
        self.model = model
        self.memory = in_memory
        self.chat_history = chats_history
        self.num = number
        self.username = username

    def chat_reply(self):
    # handle the return data to logic service
        LOGGER.info("get into the chat_reply, query:{}".format(self.query))
        chat_reply = SalesWinesAction(model=self.model, in_memory=self.memory, chats_history=self.chat_history, number=self.num, username=self.username).chat_with_database(query=self.query)
        return chat_reply

    def get_history(self):
        return SalesWinesAction().get_history()
