from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain.memory import ChatMessageHistory
from langchain.schema import messages_from_dict, messages_to_dict

from app.factories.model_factory import create_model
import config


def chat(query, model_name="OpenAI", with_memory=False, history=[]):
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
        print(f"An error occurred: {str(e)}")
