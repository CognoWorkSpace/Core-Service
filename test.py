import json
import unittest

from app import app


class ChatTestCases(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_single_chat(self):
        mock_data = {
            "query": "Hello!",
            "with_memory": False
        }
        try:
            response = self.client.post('/chat',
                                        data=json.dumps(mock_data),
                                        content_type='application/json')
            self.assertEqual(200, response.status_code)
            json_data = response.get_json()
            self.assertIn('reply', json_data)
        except AssertionError as e:
            print("Test failed. Reason:", str(e))
            raise

    def test_multi_chat(self):
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
        mock_data = {
            "query": "Hello! What's my name?",
            "history": history,
            "with_memory": True
        }
        try:
            response = self.client.post('/chat',
                                        data=json.dumps(mock_data),
                                        content_type='application/json')
            self.assertEqual(200, response.status_code)
            json_data = response.get_json()
            self.assertIn('reply', json_data, 'Didn\'t get the reply message')
            self.assertIn("Dijkstra", json_data["reply"],
                          'Expected Dijkstra in the response, but the response is {}'.format(json_data["reply"]))
        except AssertionError as e:
            print("Test failed. Reason:", str(e))
            raise

    def test_empty_query(self):

        mock_data = {
            "with_memory": True
        }
        try:
            response = self.client.post('/chat',
                                        data=json.dumps(mock_data),
                                        content_type='application/json')

            self.assertEqual(response.status_code, 400)
            json_data = response.get_json()
            self.assertEqual(json_data['error'], 'Query must not be empty.')
        except AssertionError as e:
            print("Test failed. Reason:", str(e))
            raise

    def test_invalid_model(self):

        mock_data = {
            "query": "Hello!",
            "with_memory": False,
            "model_name": "ChatGLM",
        }
        try:
            response = self.client.post('/chat',
                                        data=json.dumps(mock_data),
                                        content_type='application/json')

            self.assertEqual(response.status_code, 400)
            json_data = response.get_json()
            self.assertEqual(json_data['error'], 'Model does not exist.')
        except AssertionError as e:
            print("Test failed. Reason:", str(e))
            raise

    def test_invalid_chat_history(self):
        history = [
            {
                'type': 'Dijkstra',
                'date': {
                    'content': 'hi!'
                }
            },
            {
                'type': 'ia',
                'data': {
                    'contet': 'whats u'
                }
            }
        ]
        mock_data = {
            "query": "Hello!",
            "history": history,
            "with_memory": True
        }
        try:
            response = self.client.post('/chat',
                                        data=json.dumps(mock_data),
                                        content_type='application/json')
            self.assertEqual(400, response.status_code)
            json_data = response.get_json()
            self.assertIn('Please check the format of history message you post', json_data["error"], 'Didn\'t get the reply message')
        except AssertionError as e:
            print("Test failed. Reason:", str(e))
            raise

    def test_invalid_model(self):
        mock_data = {
            "query": "Hello!",
            "with_memory": False,
            "model_name": "Dijkstra"
        }
        try:
            response = self.client.post('/chat',
                                        data=json.dumps(mock_data),
                                        content_type='application/json')
            self.assertEqual(400, response.status_code)
            json_data = response.get_json()
            self.assertIn('Model {} does not exist.'.format(mock_data["model_name"]), json_data["error"],
                          'Didn\'t get the error message')
        except AssertionError as e:
            print("Test failed. Reason:", str(e))
            raise
