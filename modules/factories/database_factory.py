import os

from dotenv import load_dotenv
from langchain.vectorstores import Milvus
from langchain.vectorstores.pgvector import DistanceStrategy
from langchain.vectorstores.pgvector import PGVector
import const

load_dotenv()


def create_database(database_name="", collection_name="", connection_string="", embeddings="", **kwargs):

    if 'openai_api_key' not in kwargs:
        kwargs['openai_api_key'] = os.getenv("OPENAI_API_KEY")

    try:
        if database_name == const.MILVUS:
            return Milvus(embedding_function=embeddings, collection_name=collection_name, connection_args=connection_string, drop_old=False)
        else:
            raise ValueError("Database does not exist!")

    except ValueError as e:
        raise Exception(e)
