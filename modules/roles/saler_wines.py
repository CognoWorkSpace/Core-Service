from modules.actions.sale_wines import SalesWinesAction
from utils.logging import LOGGER


class SalesWines:
    def __init__(self, query=None, model=None, in_memory=None, chats_history=None, number=10):
        self.query = query
        self.model = model
        self.memory = in_memory
        self.chat_history = chats_history
        self.num = number

    def chat_reply(self):
    # handle the return data to logic service
        chat_reply = SalesWinesAction(model=self.model, in_memory=self.memory, chats_history=self.chat_history, number=self.num).chat(query=self.query)
        return chat_reply

    def get_history(self):
        return SalesWinesAction().get_history()
