from django.test import TestCase

# Create your tests here.
from chains.chat import chat

history = [
    {
        'type': 'human',
        'data': {
            'content': 'hi!',
            'additional_kwargs': {}
        }},
    {
        'type': 'ai',
        'data': {
            'content': 'whats up?',
            'additional_kwargs': {}
        }
    }
]

output = chat("GoodMorning!", history)
print(output)
