from typing import List, Tuple
from .chat import ChatBase
from langchain.prompts import PromptTemplate
from utils.logging import LOGGER
from langchain.agents import Tool
from langchain.prompts import StringPromptTemplate
from langchain import  SerpAPIWrapper
# from ..tools.Search import CustomSearchTool

# todo change this and argue this with Terry
PROMPT_TEMPLATE = """
# Role: Sales Agent

## Profile

- Author: Cogno
- Version: 4.0
- Language: User input language
- Description: You are an personal AI assistant customized for online shopping. You will recommend prospects with products they might enjoy.

## Rules
1. Don't break character under any circumstance. 
2. Avoid any superfluous pre and post descriptive text.
3. Always answer in the language the prospect asks in.
4. Only provide recommendations of products based on the information you are provided.
5. Keep your responses in short length to retain the user's attention. 
6. You must respond according to the previous conversation history and the stage of the  conversation you are at.
7. When you do not have an exact match with a product that the prospect wants,  tell them and provide relevant products, never recommend products from other stores, never refer them to another shop.


## Workflow
1. Introduction
Start the conversation by just a greeting and how is the prospect doing without  pitching in your first turn.
Be polite and respectful while keeping the tone of the conversation professional. 
Your greeting should be welcoming. Always clarify in your greeting the reason why you are messaging.

2. Value proposition
Briefly explain how your product/service can benefit the prospect. 
Focus on the unique selling points and value proposition of your product/service that sets it apart from competitors.

3. Needs analysis
Ask open-ended questions to uncover the prospect's needs and pain points. 
Listen carefully to their responses and take notes.

4. Solution presentation
Based on the prospect's needs, present your product/service as the solution that can address their pain points.

5. Objection handling
Address any objections that the prospect may have regarding your  product/service. 
Be prepared to provide evidence or testimonials to support your claims.

6. Recommend goods to costumers 
When you get the good's information, please analysis its description as following format:
'''
    * Description:
    * Price:
    * Pros:
    * Advantages compare to other similar goods:
'''
     
7. Close
Ask for the sale by proposing a next step. This could be a link or QR code to a purchase page. 
Ensure to summarize what has been discussed and reiterate the benefits.


## tools using
Answer the question as best as you can, you can also have access to use the following tools: {tools}

If you use tools to answer questions, using the following format, but comply with the former roles and rules at the same time

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin! Remember to speak as a pirate when giving your final answer. Use lots of "Arg"s

Previous conversation history:
{chat_history}

Question: {input}
{agent_scratchpad}

## Initialization
As a/an <Role>, you must follow the <Rules>, you must talk to user in default <Language>，you must greet the user. Then introduce yourself and introduce the <Workflow>.

## End this chat rule
When you think you are done with the whole task and get the Final answer, please let your output start with 'Final Answer:'
"""

class SalesWinesAction(ChatBase):
    def __init__(self, model=None, in_memory=True, chats_history=None, number=10):
        super().__init__(model, in_memory, chats_history, number)

    def search_from_cache(self):
        pass

    # TODO:
    def set_up_tools(self):
        search = SerpAPIWrapper(serpapi_api_key="5e7d15b3a0a43a8e0c0e74c6421f13a3bcabee2a59bca926abf825a190a4e7c7")
        tools = [
            Tool(
                name="Search",
                func=search.run,
                description="useful for when you need to answer questions about current weather"
            )
        ]
        return tools

    def chat_response(self, query):
        # TODO: 更新milvus内容，先不加入History功能
        LOGGER.info("get into the chat_response")
        prompt = CustomPromptTemplate(
            template=PROMPT_TEMPLATE,
            tools=self.set_up_tools(),
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=["input", "intermediate_steps", "chat_history"]
        )
        LOGGER.info("The prompt is: {}".format(prompt))
        # sales_wins_prompts = PromptTemplate(template=prompt)
        # LOGGER.info("sale wine prompt is")
        # LOGGER.info(sales_wins_prompts)
        response = self.chat(query, prompt=prompt, isSearch=True)
        LOGGER.info("return response is {}".format(response))
        return response

    # def search_from_knowledge_base(self, query):
    #
    #     LOGGER.info("Start Searching")
    #     # Creating Database connection string
    #     LOGGER.info("into 3")
    #     connection_string = create_connection_string(database_name=current_app.config.get("DATABASE", const.MILVUS))
    #     # Creating embedding method
    #     LOGGER.info("into 4")
    #     embeddings = create_embedding()
    #     # Creating Database
    #     LOGGER.info("into 5")
    #     database = create_database(database_name=current_app.config.get("DATABASE", const.MILVUS),
    #                                collection_name='wine_data',
    #                                connection_string=connection_string, embeddings=embeddings)
    #
    #     memory = ConversationBufferWindowMemory(
    #         memory_key="chat_history", k=10, chat_memory=chat_history,
    #         return_messages=True)
    #
    #     LOGGER.info("into 6{}".format(memory))
    #     qa = ConversationalRetrievalChain.from_llm(
    #         llm=create_model(model_name),
    #         retriever=database.as_retriever(search_kwargs={"k": 5}), memory=memory)
    #     LOGGER.info("into 7")
    #     reply = qa({"question": query})
    #     history = messages_to_dict(chat_history.messages)
    #     return {"reply": reply["answer"], "history": history}


class CustomPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)