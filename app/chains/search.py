from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_from_dict, messages_to_dict

from ..factories.connection_string_factory import create_connection_string
from ..factories.embedding_factory import create_embedding
from ..factories.database_factory import create_database
from ..factories.model_factory import create_model
import config


def search(query, model_name="OpenAI", with_memory=False, history=[], collection_name=None):

    connection_string = create_connection_string(database_name="postgres")
    embeddings = create_embedding()
    database = create_database(database_name="postgres", collection_name=collection_name,
                               connection_string=connection_string, embeddings=embeddings)
    # Convert dics to message object
    chat_history = ChatMessageHistory()
    messages = messages_from_dict(history)

    # Add every message to history Object
    for message in messages:
        chat_history.add_message(message=message)

    # Create memory object that only keep 5 closest messages
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history", k=config.BUFFER_TOP_K, chat_memory=chat_history, return_messages=True)

    qa = ConversationalRetrievalChain.from_llm(
        llm=create_model(model_name), retriever=database.as_retriever(search_kwargs={"k": 3}), memory=memory)

    result = qa({"question": query})
    reply = result['answer']
    print(result)

    history = messages_to_dict(chat_history.messages)

    return {"reply": reply, "history": history}
