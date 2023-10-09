from modules.actions.inform import InformAction
from utils.logging import LOGGER


class Informer:
    def __init__(self, query=None, model=None, in_memory=None, chat_history_dict=None, number=10):
        self.query = query
        self.model = model
        self.memory = in_memory
        self.chat_history_dict = chat_history_dict
        self.num = number

    def chat_reply_given_history(self):
    # handle the return data to logic service
        LOGGER.info("get into the informer_chat_reply")
        if self.chat_history_dict == None:
            chat_reply = InformAction(model=self.model, in_memory=self.memory, chat_history_dict=self.chat_history_dict,
                                  number=self.num).chat_with_pdf(query=self.query)
        else:
            chat_reply = InformAction(model=self.model, in_memory=self.memory, chat_history_dict=self.chat_history_dict, number=self.num).chat_with_pdf_given_history(query=self.query)
        return chat_reply

    def get_history(self):
        return InformAction().get_history()
