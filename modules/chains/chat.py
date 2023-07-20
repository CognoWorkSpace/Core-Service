from langchain.chains import ConversationChain
from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import messages_from_dict, messages_to_dict

import const
from init import conf
from modules.factories.model_factory import create_model

from utils.logging import LOGGER


def chat(query, model_name, with_memory, history):
    if model_name is None:
        model_name = conf().get(key="MODEL", default=const.OPENAI)
    if with_memory is None:
        with_memory = False
    if history is None:
        history = []

    LOGGER.info(
        "Chat function starts with query: {}, model_name: {}, with_memory: {}, history length: {}.".format(query,
                                                                                                           model_name,
                                                                                                           with_memory,
                                                                                                           len(history)))
    try:
        # Convert dicts to message object
        chat_history = ChatMessageHistory()
        try:
            messages = messages_from_dict(history)
        except Exception as e:
            LOGGER.error("User provided an invalid chat history: {}".format(e))
            raise ValueError("Please check the format of history message you post: {}".format(e))
        # Add every message to history Object
        for message in messages:
            chat_history.add_message(message=message)
        LOGGER.info("Chat history converted.")

        # Create memory object that only keep 5 closest messages
        memory = ConversationBufferWindowMemory(
            k=conf().get(key="OPENAI_BUFFER_TOP_K", default=5), chat_memory=chat_history)

        LOGGER.info("Memory object created.")

        # Create a Conversation Chain
        conversation = ConversationChain(
            llm=create_model(model_name),
            verbose=True,
            memory=memory,
        )

        LOGGER.info("Conversation Chain created.")

        # Get the reply(string) from the conversation Chain
        reply = conversation.predict(input=query)

        LOGGER.info("Reply generated: {}".format(reply))

        history = messages_to_dict(chat_history.messages)

        chat_history.clear()

        LOGGER.info("Chat function ends.")

        return {"reply": reply, "history": history}
    except ValueError as e:
        raise ValueError(e)
    except Exception as e:
        LOGGER.error("An unexpected error occurred in chat function: {}".format(e))
        raise Exception(e)

