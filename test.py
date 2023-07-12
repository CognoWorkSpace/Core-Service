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
    output = chat(query="Good Morning! What's my name?", model_name="OpenAI",
                  with_memory=False, history=history)
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
                'content': ''
            }
        },
        {
            'type': 'ai',
            'data': {
                'content': ''
            }
        }
    ]
    collection_name = "split"
    output = search(query="”", model_name="OpenAI",
                    with_memory=True, history=[], collection_name=collection_name)
    print(output)


def upload_test():
    return


if __name__ == "__main__":
    memory_chat_test()  # 调试chat_with_memory的过程
    # search_test()
