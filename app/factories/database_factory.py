import config
from langchain.vectorstores.pgvector import PGVector

from langchain.vectorstores.pgvector import DistanceStrategy


def create_database(database_name="postgres", collection_name="", connection_string="", embeddings="", **kwargs):

    if 'openai_api_key' not in kwargs:
        kwargs['openai_api_key'] = config.OPENAI_API_KEY

    if database_name == "postgres":
        return PGVector.from_existing_index(
            collection_name=collection_name,
            connection_string=connection_string,
            distance_strategy=DistanceStrategy.COSINE,
            openai_api_key=config.OPENAI_API_KEY,
            embedding=embeddings
        )
    else:
        raise ValueError("Database does not exist!")
