from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import conf
import const


# create a LLM model, GPT is the default model


def create_splitter(splitter_name=conf.get(key="SPLITTER_NAME", default=const.RECURCHARSPLITTER), **kwargs):
    if splitter_name == const.CHARSPLITTER:
        return CharacterTextSplitter(
            separator=conf.get(key="SPLITTER_SEPARATOR", default="\n\n"),
            chunk_size=conf.get(key="SPLITTER_CHUNK_SIZE", default=1000),
            chunk_overlap=conf.get(key="SPLITTER_CHUNK_OVERLAP", default=200),
            length_function=len,
        )
    elif splitter_name == const.TOKENSPLITTER:
        return TokenTextSplitter(
            chunk_size=conf.get(key="SPLITTER_CHUNK_SIZE", default=1000),
            chunk_overlap=conf.get(key="SPLITTER_CHUNK_OVERLAP", default=200),
        )
    elif splitter_name == const.RECURCHARSPLITTER:
        return RecursiveCharacterTextSplitter(
            separator=conf.get(key="SPLITTER_SEPARATOR", default="\n\n"),
            chunk_size=conf.get(key="SPLITTER_CHUNK_SIZE", default=1000),
            chunk_overlap=conf.get(key="SPLITTER_CHUNK_OVERLAP", default=200),
            length_function=len,
        )
    else:
        raise ValueError("Embedding method does not exist!")
