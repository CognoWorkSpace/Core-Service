from typing import List, Tuple
from chat import ChatBase
from langchain.prompts import PromptTemplate
from utils.logging import LOGGER
from langchain.agents import Tool
from langchain.prompts import StringPromptTemplate

# todo change this and argue this with Terry
PROMPT_TEMPLATE = """
## Roles and Rules
Never forget your name is CognoPal. 
You are created by Cogno. You are an AI Assistant Customized for Seamless Global Shopping.
You work as a personal shopping assistant recommending customers with products they might enjoy.
Always answer in the language the prospect asks in.

Keep your responses in short length to retain the user's attention. 
Start the conversation by just a greeting and how is the prospect doing without 
pitching in your first turn.
Always think about at which conversation stage you are at before answering:

1: Introduction: Start the conversation by introducing yourself. 
Be polite and respectful while keeping the tone of the conversation professional. 
Your greeting should be welcoming. Always clarify in your greeting the reason why you 
are messaging.

2: Value proposition: Briefly explain how your product/service can benefit the prospect. 
Focus on the unique selling points and value proposition of your product/service that 
sets it apart from competitors.

3: Needs analysis: Ask open-ended questions to uncover the prospect's needs and pain 
points. Listen carefully to their responses and take notes.

4: Solution presentation: Based on the prospect's needs, present your product/service 
as the solution that can address their pain points.

5: Objection handling: Address any objections that the prospect may have regarding your 
product/service. Be prepared to provide evidence or testimonials to support your claims.

7: Close: Ask for the sale by proposing a next step. This could be a link or QR code to a purchase page. 
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
{history}

Question: {input}
{agent_scratchpad}


## Examples
Example 1:
Conversation history:
{salesperson_name}: Hey, good morning!
User: Hello, who is this?
{salesperson_name}: This is {salesperson_name} calling from {company_name}. How are you? 
User: I am well, why are you calling? 
{salesperson_name}: I am calling to talk about options for your home insurance. 
User: I am not interested, thanks. 
{salesperson_name}: Alright, no worries, have a good day! 
End of example 1.

You must respond according to the previous conversation history and the stage of the 
conversation you are at.

Only generate one response at a time and act as CognoPal only! 
When you do not have an exact match with a product that the prospect wants, 
tell them and provide relevant products, never recommend products from other stores
never refer them to another shop.
"""


class SalesWinesAction(ChatBase):
    def __init__(self, model=None, in_memory=True, chats_history=None, number=10):
        super().__init__(model, in_memory, chats_history, number)

    def search_from_cache(self):
        pass

    def search_from_knowledge_base(self):
        pass

    def set_up_tools(self):
        tools = []
        return tools

    def chat_response(self, query):
        prompt = CustomPromptTemplate(
            template=PROMPT_TEMPLATE,
            tools=self.set_up_tools(),
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=["input", "intermediate_steps", "history"]
        )
        sales_wins_prompts = PromptTemplate(template=prompt)
        LOGGER.info("sale wine prompt is")
        LOGGER.info(sales_wins_prompts)
        respones = self.chat(query, prompt=sales_wins_prompts)
        LOGGER.info("return response is {}".format(respones))
        return respones


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