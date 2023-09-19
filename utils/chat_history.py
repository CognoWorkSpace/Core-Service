# -*- coding: utf-8 -*-
# File : chat_history.py
# Time : 2023/9/13 15:10 
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

from langchain.memory import ChatMessageHistory



chat_histories = {}

def get_or_create_chat_history(key):

    if key not in chat_histories:
        chat_histories[key] = ChatMessageHistory()
    return chat_histories[key]