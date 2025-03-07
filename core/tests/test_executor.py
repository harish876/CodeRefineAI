import unittest
from core.executor import Executor, ExecutorResponse
from core.executor.config import load_settings
import pandas as pd

class TestExecutorIntegration(unittest.TestCase):

    def setUp(self):
        self.settings = load_settings("/Users/harishgokul/CodeRefineAI/.env")
        self.executor = Executor(self.settings)

    def test_execute_code(self):
        code = """
def add(a, b):
    return a + b

print(add(1, 2))
"""
        # Execute the code
        response = self.executor.execute_code(
            code="print('Hello, world!')",
            test_cases="",
            expected_results="Hello, world!",
        )

        # Print the response for debugging purposes
        print(response)

        # Assert the response status
        self.assertEqual(response.status, "success")
        self.assertIsNotNone(response.token)
        
        # Get the submission details using the token
        submission_details = self.executor.poll_submission_status(response.token)
        print(submission_details)

        # Print the submission details for debugging purposes
        print(submission_details.json())

        # Assert the submission details status
        self.assertEqual(submission_details.status_code, 200)
        self.assertIn("stdout", submission_details.json())

if __name__ == '__main__':
    unittest.main()