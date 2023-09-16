import os

from langchain.chat_models import ChatOpenAI


import const

from utils.logging import LOGGER

# create a LLM model, GPT is the default model
from flask import current_app

def create_model(model_name="", **kwargs):

    if 'openai_model_name' not in kwargs:
        kwargs['openai_model_name'] = current_app.config.get("OPENAI_MODEL_NAME", "gpt-3.5-turbo")

    if 'openai_api_key' not in kwargs:
        kwargs['openai_api_key'] = os.getenv("OPENAI_API_KEY")

    if 'max_tokens' not in kwargs:
        kwargs['max_tokens'] = current_app.config.get("OPENAI_MAX_TOKENS", 1024)

    if 'temperature' not in kwargs:
        kwargs['temperature'] = current_app.config.get("OPENAI_TEMPERATURE", 0.7)
    if model_name == const.OPENAI:
        LOGGER.info("Model {} is created".format(model_name))
        return ChatOpenAI(model_name=kwargs['openai_model_name'], openai_api_key=kwargs['openai_api_key'],
                          max_tokens=kwargs['max_tokens'], temperature=kwargs['temperature'])
    else:
        LOGGER.error("User used an invalid model: {}".format(model_name))
        raise ValueError("Model {} does not exist.".format(model_name))
