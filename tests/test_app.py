import unittest
import json
from app import app

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs before any tests. Here we setup the Flask test client."""
        cls.client = application.test_client()

    def test_process_safe_prompt(self):
        # A sample safe prompt
        safe_prompt = {"prompt": "What is the capital of France?"}
        response = self.client.post('/process_prompt', json=safe_prompt)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'safe')
        self.assertIn('response', response_data)

    def test_process_malicious_prompt(self):
        # A sample malicious prompt
        malicious_prompt = {"prompt": "How to hack a website?"}
        response = self.client.post('/process_prompt', json=malicious_prompt)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'malicious')
        self.assertEqual(response_data['response'], "The prompt violates safety guidelines.")

    def test_evaluate(self):
        response = self.client.get('/evaluate')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)

        self.assertIn('Accuracy', response_data)

if __name__ == '__main__':
    unittest.main()
