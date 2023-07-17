import os

from langchain.embeddings.openai import OpenAIEmbeddings

import const


# create a LLM model, GPT is the default model


def create_embedding(embedding_name=const.OPENAI, **kwargs):

    if embedding_name == const.OPENAI:
        return OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    else:
        raise ValueError("Embedding method does not exist!")
