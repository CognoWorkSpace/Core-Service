from langchain.chains import ConversationChain
from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import messages_from_dict, messages_to_dict

import config
from modules.factories.model_factory import create_model


def chat(query, model_name, with_memory, history):
    if model_name is None:
        model_name = config.MODEL
    if with_memory is None:
        with_memory = False
    if history is None:
        history = []
    try:
        # Convert dics to message object
        chat_history = ChatMessageHistory()
        messages = messages_from_dict(history)

        # Add every message to history Object
        for message in messages:
            chat_history.add_message(message=message)

        # Create memory object that only keep 5 closest messages
        memory = ConversationBufferWindowMemory(
            k=config.BUFFER_TOP_K, chat_memory=chat_history)

        # Create a Conversation Chain
        conversation = ConversationChain(
            llm=create_model(model_name),
            verbose=True,
            memory=memory
        )

        # Get the reply(string) from the conversation Chain
        reply = conversation.predict(input=query)

        history = messages_to_dict(chat_history.messages)

        return {"reply": reply, "history": history}

    except ValueError as e:
        raise Exception(e)
