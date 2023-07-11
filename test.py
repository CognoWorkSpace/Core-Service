from django.test import TestCase
from app.chains.chat import chat
from app.chains.search import search
import json


def memory_chat_test():
    history = [
        {
            'type': 'human',
            'data': {
                'content': 'hi!'
            }
        },
        {
            'type': 'ai',
            'data': {
                'content': 'whats up?'
            }
        },
        {
            'type': 'human',
            'data': {
                'content': 'I am Dijkstra'
            }
        },
        {
            'type': 'ai',
            'data': {
                'content': 'Hello Dijkstra'
            }
        }
    ]
    output = chat(query="Good Morning!", model_name="OpenAI",
                  with_memory=False, history=[])
    print(json.dumps(output))


def search_test():
    history = [
        {
            'type': 'human',
            'data': {
                'content': '你好！'
            }
        },
        {
            'type': 'ai',
            'data': {
                'content': '你好啊！'
            }
        },
        {
            'type': 'human',
            'data': {
                'content': '什么是反洗钱'
            }
        },
        {
            'type': 'ai',
            'data': {
                'content': '洗钱是一种防止非法资金流动的措施。它是指通过监测和阻止非法资金进入合法金融系统，以及追踪和阻止非法资金从合法金融系统流出的行动。该措施旨在减少洗钱活动、恐怖主义融资和其他非法金融活动的风险。'
            }
        }
    ]
    collection_name = "split"
    output = search(query="金融机构如何开展“法人金融机构洗钱和恐怖融资风险自评估”", model_name="OpenAI",
                    with_memory=True, history=[], collection_name=collection_name)
    print(output)


# def upload_test(){
# }
if __name__ == "__main__":
    # memory_chat_test()  # 调试chat_with_memory的过程
    search_test()
