import os

from langchain.chat_models import ChatOpenAI

from init import conf
import const


# create a LLM model, GPT is the default model


def create_model(model_name=conf().get(key="MODEL", default=const.OPENAI), **kwargs):

    if 'openai_model_name' not in kwargs:
        kwargs['openai_model_name'] = conf().get(key="OPENAI_MODEL_NAME", default="gpt-3.5-turbo")

    if 'openai_api_key' not in kwargs:
        kwargs['openai_api_key'] = os.getenv("OPENAI_API_KEY")

    if 'max_tokens' not in kwargs:
        kwargs['max_tokens'] = conf().get(key="OPENAI_MAX_TOKENS", default=1024)

    if 'temperature' not in kwargs:
        kwargs['temperature'] = conf().get(key="OPENAI_TEMPERATURE", default=0.7)

    # TODO: log记录config name...
    # TODO: 大小写 .contains constant
    if model_name == const.OPENAI:
        return ChatOpenAI(model_name=kwargs['openai_model_name'], openai_api_key=kwargs['openai_api_key'],
                          max_tokens=kwargs['max_tokens'], temperature=kwargs['temperature'])
    else:
        raise ValueError("Model does not exist.")
