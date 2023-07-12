from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_from_dict, messages_to_dict

from app.factories.connection_string_factory import create_connection_string
from app.factories.embedding_factory import create_embedding
from app.factories.database_factory import create_database
from app.factories.model_factory import create_model
import config


def search(query, model_name=config.MODEL, with_memory=False, history=[], collection_name=None):

    # Creating Milvus connection string
    connection_string = create_connection_string(database_name=config.DATABASE)
    # Creating embedding method
    embeddings = create_embedding()
    # Creating Milvus Database
    database = create_database(database_name=config.DATABASE, collection_name=collection_name,
                               connection_string=connection_string, embeddings=embeddings)

    # Convert a dics to message object
    chat_history = ChatMessageHistory()
    messages = messages_from_dict(history)

    # Add every message to history Object
    for message in messages:
        chat_history.add_message(message=message)

    # Create a memory object that only keep 5 closest messages
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history", k=config.BUFFER_TOP_K, chat_memory=chat_history, return_messages=True)

    # Create a  Coversation Retrieval Chain
    qa = ConversationalRetrievalChain.from_llm(
        llm=create_model(model_name), retriever=database.as_retriever(search_kwargs={"k": config.BUFFER_TOP_K}), memory=memory)

    result = qa({"question": query})
    reply = result['answer']

    history = messages_to_dict(chat_history.messages)

    return {"reply": reply, "history": history}
