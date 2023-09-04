# -*- coding: utf-8 -*-
# File : Calculator.py
# Time : 2023/9/1 9:17 
# Author : Dijkstra Liu
# Email : l.tingjun@wustl.edu
# 
# 　　　    /＞ —— フ
# 　　　　　| `_　 _ l
# 　 　　　ノ  ミ＿xノ
# 　　 　 /　　　 　|
# 　　　 /　 ヽ　　ﾉ
# 　 　 │　　|　|　\
# 　／￣|　　 |　|　|
#  | (￣ヽ＿_ヽ_)__)
# 　＼_つ
#
# Description:
from langchain.agents import Tool
from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field
# Import things that are needed generically
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from pydantic import BaseModel, Field

from ..factories.model_factory import create_model



llm_math_chain = LLMMathChain(llm=create_model(model_name="OpenAI"), verbose=True)
class CustomCalculatorTool(BaseTool):
    name = "Calculator"
    description = "useful for when you need to answer questions about math"
    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return llm_math_chain.run(query)

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Calculator does not support async")
