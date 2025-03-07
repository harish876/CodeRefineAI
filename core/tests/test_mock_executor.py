import unittest
from unittest.mock import patch, MagicMock
from core.executor.executor import Executor, ExecutorResponse
from core.executor.config import Settings, load_settings
import pandas as pd

class TestExecutor(unittest.TestCase):

    def setUp(self):
        self.settings = load_settings("/Users/harishgokul/CodeRefineAI/.env")
        print(self.settings)
        self.executor = Executor(self.settings)

    @patch('core.executor.executor.requests.post')
    def test_submit(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"token": "test_token"}
        mock_post.return_value = mock_response

        response = self.executor._submit(
            raw_source_code="print('Hello, world!')",
            test_cases="",
            expected_results="Hello, world!",
            language="python"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["token"], "test_token")

    @patch('core.executor.executor.requests.get')
    def test_get_submission_details(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_get.return_value = mock_response

        response = self.executor.get_submission_details("test_token")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    @patch('core.executor.executor.Executor._submit')
    def test_execute(self, mock_submit):
        mock_response = MagicMock()
        mock_response.json.return_value = {"token": "test_token"}
        mock_submit.return_value = mock_response

        metadata = pd.Series({
            "question_id": 1,
            "name": "Example Question",
            "setup_code": "class TestCaseGenerator: ...",
            "entry_point": "main",
            "import_code": "import sys",
            "test_cases": [{"input": "1 2", "output": "3"}]
        })

        response = self.executor.execute(
            code_template="def {entry_point}():\n    {import_code}\n    {solution_code}\n    {test_case_code}",
            solution_code="print('Hello, world!')",
            metadata=metadata
        )

        self.assertEqual(response.status, "success")
        self.assertEqual(response.token, "test_token")

    @patch('core.executor.executor.Executor._submit')
    def test_execute_code(self, mock_submit):
        mock_response = MagicMock()
        mock_response.json.return_value = {"token": "test_token"}
        mock_submit.return_value = mock_response

        response = self.executor.execute_code(
            code="print('Hello, world!')",
            test_cases="",
            expected_results="Hello, world!"
        )

        self.assertEqual(response.status, "success")
        self.assertEqual(response.token, "test_token")

if __name__ == '__main__':
    unittest.main()