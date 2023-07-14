import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

import config

load_dotenv()

# create a LLM model, GPT is the default model


def create_model(model_name=config.MODEL, **kwargs):

    if 'openai_model_name' not in kwargs:
        kwargs['openai_model_name'] = config.OPENAI_MODEL_NAME

    if 'openai_api_key' not in kwargs:
        kwargs['openai_api_key'] = os.getenv("OPENAI_API_KEY")

    if 'max_tokens' not in kwargs:
        kwargs['max_tokens'] = config.OPENAI_MAX_TOKENS

    if 'temperature' not in kwargs:
        kwargs['temperature'] = config.OPENAI_TEMPERATURE

    if model_name == "OpenAI":
        return ChatOpenAI(model_name=kwargs['openai_model_name'], openai_api_key=kwargs['openai_api_key'], max_tokens=kwargs['max_tokens'], temperature=kwargs['temperature'])
    else:
        raise ValueError("Model does not exist.")
