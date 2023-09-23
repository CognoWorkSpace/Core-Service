from modules.actions.somme_wines import SommeAction
from utils.logging import LOGGER


class ConWines:
    def __init__(self, query=None, model=None, in_memory=None, chats_history=None, number=10):
        self.query = query
        self.model = model
        self.memory = in_memory
        self.chat_history = chats_history
        self.num = number

    def chat_reply(self):
    # handle the return data to logic service
        LOGGER.info("get into the chat_reply")
        chat_reply = SommeAction(model=self.model, in_memory=self.memory, chats_history=self.chat_history, number=self.num).chat(query=self.query)
        return chat_reply

    def get_history(self):
        return SommeAction().get_history()
