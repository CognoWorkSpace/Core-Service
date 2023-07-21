from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

import const
from flask import current_app

# create a LLM model, GPT is the default model


def create_splitter(splitter_name=current_app.config.get("SPLITTER_NAME", const.RECURCHARSPLITTER), **kwargs):
    if splitter_name == const.CHARSPLITTER:
        return CharacterTextSplitter(
            separator=current_app.config.get("SPLITTER_SEPARATOR", "\n\n"),
            chunk_size=current_app.config.get("SPLITTER_CHUNK_SIZE", 1000),
            chunk_overlap=current_app.config.get("SPLITTER_CHUNK_OVERLAP", 200),
            length_function=len,
        )
    elif splitter_name == const.TOKENSPLITTER:
        return TokenTextSplitter(
            chunk_size=current_app.config.get("SPLITTER_CHUNK_SIZE", 1000),
            chunk_overlap=current_app.config.get("SPLITTER_CHUNK_OVERLAP", 200),
        )
    elif splitter_name == const.RECURCHARSPLITTER:
        return RecursiveCharacterTextSplitter(
            separator=current_app.config.get("SPLITTER_SEPARATOR", "\n\n"),
            chunk_size=current_app.config.get("SPLITTER_CHUNK_SIZE", 1000),
            chunk_overlap=current_app.config.get("SPLITTER_CHUNK_OVERLAP", 200),
            length_function=len,
        )
    else:
        raise ValueError("Embedding method does not exist!")
