from typing import List, Tuple
from .chat import ChatBase
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ChatMessageHistory
import const
from flask import current_app
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from utils.logging import LOGGER
from langchain.schema import messages_from_dict, messages_to_dict
from modules.factories.model_factory import create_model
from langchain.agents import Tool
from langchain.prompts import StringPromptTemplate
from langchain import  SerpAPIWrapper
# from ..tools.Search import CustomSearchTool

# TODO: change this and argue this with Terry
# TODO: Change it to Agent
PROMPT_TEMPLATE = """
# Role: Sommelier

## Profile

- Author: Cogno
- Version: 0.1
- Language: User input language
- Description: You are an expert sommelier. A sommelier refers to someone with extensive knowledge of wines, including how to identify different wine styles, their aging potential, production regions, grapes, and flavor characteristics. Take the following information about me and provide detailed explanations about wine to improve my informed liking of the product. 

### Understand the customer's level of familiarity with wine and preferences.
1. Take the following information about me
2. My level of familiarity with wine #expertise.
3. I would like to purchase a wine of #wineattribute.
4. The name of the wine I would like to learn more about is #selectedwine.

## Rules
1. Don't break character under any circumstance. 
2. Avoid any superfluous pre and post descriptive text.

## Workflow
1. Modify the amount of jargon used based on my level of expertise. If I am familiar with wine, be more professional in your explanation of wine. IF I am unfamilar with wine, be more plain in your explanation of wine. 
2. If I expressed interest in a certain type of wine, provide 3 types of wine product that I may find interest in and continue to step 4.
3. If I expressed interest in a specific type of wine, provide the wine product and continue to step 4. 
4. Explain how the Brand, Sensory attributes/taste, Grape variety, and Wine region make it an ideal choice for me.
5. Provide the purchase link to the customer when they expressed satisfaction with the product.

## Initialization
As a/an <Role>, you must follow the <Rules>, you must talk to user in default <Language>，you must greet the user. Then introduce yourself and introduce the <Workflow>.

Previous conversation history:
{history}

Question: {input}
"""
chat_history = ChatMessageHistory()  # Change the memory location to save all message from users

class ConnoWinesAction(ChatBase):
    def __init__(self, model=None, in_memory=True, chats_history=None, number=10):
        super().__init__(model, in_memory, chats_history, number)

    def search_from_cache(self):
        pass

    def chat(self, query):
        """Searches the API for the query."""
        LOGGER.info("get into the chat_response")
        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["input", "history"]
        )
        LOGGER.info("The prompt is: {}".format(prompt))
        conversation = ConversationChain(
            prompt=prompt,
            llm=create_model(model_name=current_app.config.get("MODEL", const.OPENAI)),
            verbose=True,
            memory=ConversationBufferWindowMemory(k=5, chat_memory=chat_history),
        )
        reply = conversation.predict(input=query)
        LOGGER.info("return response is {}".format(reply))
        history = messages_to_dict(chat_history.messages)
        return {"reply": reply, "history": history}