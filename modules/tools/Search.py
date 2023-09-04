# -*- coding: utf-8 -*-
# File : Search.py
# Time : 2023/9/1 9:58 
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



from pydantic import BaseModel, Field
# Import things that are needed generically
from langchain import LLMMathChain, SerpAPIWrapper
from langchain.tools import BaseTool


from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

search = SerpAPIWrapper(serpapi_api_key="5e7d15b3a0a43a8e0c0e74c6421f13a3bcabee2a59bca926abf825a190a4e7c7")
class CustomSearchTool(BaseTool):
    name = "custom_search"
    description = "useful for when you need to answer questions about current events"

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return search.run(query)

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")