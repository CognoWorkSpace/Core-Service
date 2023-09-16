from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import messages_from_dict, messages_to_dict
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser, Agent
from langchain.chains import ConversationalRetrievalChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re
import const

from databaseMod.milvusDB import MilvusDB
from flask import current_app
from modules.factories.connection_string_factory import create_connection_string
from modules.factories.database_factory import create_database
from modules.factories.embedding_factory import create_embedding
from modules.factories.model_factory import create_model
from langchain import PromptTemplate
from utils.logging import LOGGER

from utils.chat_history import get_or_create_chat_history




class ChatBase:
    def __init__(self, model=None, in_memory=None, chats_history=None, number=None, username="default"):
        self.model_name = model
        self.with_memory = in_memory
        self.history = chats_history
        self.num = number
        self.username = username

    def convert_message(self, history):
        try:
            messages = messages_from_dict(history)
        except Exception as e:
            LOGGER.error("User provided an invalid chat history: {}".format(e))
            raise ValueError("Please check the format of history message you post: {}".format(e))
            # Add every message to history Object
        for message in messages:
            get_or_create_chat_history(self.username).add_message(message=message)
        LOGGER.info("Chat history converted.")

    def keep_memory_message(self, num, with_memory):
        memory = ConversationBufferWindowMemory(
            k=current_app.config.get("OPENAI_BUFFER_TOP_K", num) if with_memory else 0, chat_memory=get_or_create_chat_history(self.username),
            memory_key="chat_history", input_key="input")
        LOGGER.info("Memory object created.")
        return memory

    def chat_with_database(self, query):
        pass

    def database_search(self, query):
        pass

    def chat(self, query, prompt="", isSearch=False):
        pass

    def get_history(self):
        return messages_to_dict(get_or_create_chat_history(self.username).messages)
    def search_from_cache(self):
        pass

    def set_up_tools(self):
        pass

    class CustomOutputParser(AgentOutputParser):
        def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
            # Check if agent should finish
            if "Final Answer:" in llm_output:
                return AgentFinish(
                    # Return values is generally always a dictionary with a single `output` key
                    # It is not recommended to try anything else at the moment :)
                    return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                    log=llm_output,
                )
            # Parse out the action and action input
            regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
            match = re.search(regex, llm_output, re.DOTALL)
            if not match:
                raise OutputParserException(f"Could not parse LLM output: `{llm_output}`")
            action = match.group(1).strip()
            action_input = match.group(2)
            # Return the action and action input
            return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)
