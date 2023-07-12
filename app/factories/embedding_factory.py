import os
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

# create a LLM model, GPT is the default model


def create_embedding(embedding_name="OpenAI", **kwargs):

    if embedding_name == "OpenAI":
        return OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    else:
        raise ValueError("Embedding method does not exist!")
