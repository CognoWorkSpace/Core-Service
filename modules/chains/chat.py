from langchain.chains import ConversationChain
from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import messages_from_dict, messages_to_dict

import const
from flask import current_app
from modules.factories.model_factory import create_model

from utils.logging import LOGGER

# TODO: try to connect to MYSQL to acquire history message based on database. The test implementation is let all the user share one common history message.
chat_history = ChatMessageHistory()  # Change the memory location to save all message from users


def chat(query, model_name, with_memory, history):
    if model_name is None:
        model_name = current_app.config.get("MODEL", const.OPENAI)
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
            k=current_app.config.get("OPENAI_BUFFER_TOP_K", 5) if with_memory else 0, chat_memory=chat_history)
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

        LOGGER.info("Chat function ends.")

        return {"reply": reply, "history": history}
    except ValueError as e:
        raise ValueError(e)
    except Exception as e:
        LOGGER.error("An unexpected error occurred in chat function: {}".format(e))
        raise Exception(e)


def get_history():
    return messages_to_dict(chat_history.messages)
