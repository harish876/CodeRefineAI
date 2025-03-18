import unittest
import pandas as pd
from coderefineai_executor import Executor, load_settings, CODE_TEMPLATE

class TestExecutorIntegration(unittest.TestCase):

    def setUp(self):
        self.settings = load_settings("/Users/harishgokul/CodeRefineAI/.env")
        self.executor = Executor(self.settings)

    def test_execute_code(self):
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
    
    
    def test_execute(self):
        metadata = pd.Series({
            "question_id":134,
            "name":"gas-station",
            "setup_code": "class TestCaseGenerator:\n    def generate(self) -> dict:\n        # Generate a test case that is within a reasonable range.\n        n = random.randint(1, 10)  # chose 1 to 10 for simplicity\n        gas = [random.randint(0, 10) for _ in range(n)]\n        cost = [random.randint(0, 10) for _ in range(n)]\n        return {'gas': gas, 'cost': cost}\n\n    def encode_input(self, input_obj) -> str:\n        # Convert a test case input into a string\n        return f\"{input_obj['gas']}|{input_obj['cost']}\"\n\n    def encode_output(self, output_obj) -> str:\n        # Convert a test case output into a string\n        return str(output_obj)\n\n    def decode_input(self, input_str) -> dict:\n        # Convert a test case input string into a Python dict\n        gas_str, cost_str = input_str.split('|')\n        gas = list(map(int, gas_str.strip('[]').split(', ')))\n        cost = list(map(int, cost_str.strip('[]').split(', ')))\n        return {'gas': gas, 'cost': cost}\n\n# Example:\n# generator = TestCaseGenerator()\n# print(generator.generate())\n# print(generator.encode_input({'gas': [1, 2, 3], 'cost': [3, 2, 1]}))",
            "entry_point":"canCompleteCircuit",
            "import_code":"from typing import List\nimport random",
            "test_cases": "{\"input\": \"[4, 6]|[9, 1]\", \"output\": \"1\"}\n{\"input\": \"[5, 7, 9, 2, 6]|[5, 0, 6, 10, 0]\", \"output\": \"0\"}\n{\"input\": \"[5, 0, 8]|[8, 0, 2]\", \"output\": \"1\"}\n{\"input\": \"[10, 7, 3]|[10, 2, 7]\", \"output\": \"0\"}\n{\"input\": \"[7, 8]|[7, 0]\", \"output\": \"0\"}\n{\"input\": \"[3, 8, 0, 9, 2, 3, 7]|[3, 1, 2, 3, 2, 6, 1]\", \"output\": \"0\"}\n{\"input\": \"[7, 2, 4]|[9, 10, 6]\", \"output\": \"-1\"}\n{\"input\": \"[4, 7, 9, 1]|[5, 5, 6, 10]\", \"output\": \"-1\"}\n{\"input\": \"[10, 1]|[2, 4]\", \"output\": \"0\"}\n{\"input\": \"[1, 5, 0, 9]|[5, 4, 1, 0]\", \"output\": \"1\"}\n{\"input\": \"[0, 9, 4, 0, 5, 6, 4, 2, 10, 7]|[5, 10, 3, 2, 10, 9, 1, 4, 3, 1]\", \"output\": \"-1\"}\n{\"input\": \"[1, 3, 3, 5, 5]|[8, 4, 3, 3, 0]\", \"output\": \"-1\"}\n{\"input\": \"[7, 8, 0, 2]|[4, 6, 2, 9]\", \"output\": \"-1\"}\n{\"input\": \"[8, 10, 8, 6, 9, 7, 5, 9, 5, 3]|[4, 4, 5, 7, 1, 2, 1, 3, 4, 1]\", \"output\": \"0\"}\n{\"input\": \"[10, 0, 2, 7]|[2, 4, 3, 4]\", \"output\": \"0\"}\n{\"input\": \"[3, 7, 10]|[5, 8, 7]\", \"output\": \"2\"}\n{\"input\": \"[6, 3, 8, 3, 7, 2]|[8, 1, 7, 8, 3, 9]\", \"output\": \"-1\"}\n{\"input\": \"[0, 7, 4, 7, 1, 8, 8, 8, 3]|[4, 3, 5, 7, 3, 6, 4, 6, 5]\", \"output\": \"1\"}\n{\"input\": \"[0]|[0]\", \"output\": \"0\"}\n{\"input\": \"[4, 7, 8, 4, 8, 7, 7, 7]|[10, 7, 5, 8, 7, 1, 0, 0]\", \"output\": \"4\"}\n{\"input\": \"[10, 5, 3]|[1, 7, 8]\", \"output\": \"0\"}\n{\"input\": \"[6, 3, 5, 0, 6, 8, 1]|[10, 3, 9, 4, 10, 10, 3]\", \"output\": \"-1\"}\n{\"input\": \"[1, 4, 9, 10]|[10, 0, 4, 9]\", \"output\": \"1\"}\n{\"input\": \"[1, 8, 8, 0, 6, 9, 5]|[5, 5, 7, 8, 10, 1, 1]\", \"output\": \"5\"}\n{\"input\": \"[10, 3, 0, 0, 10, 10, 9, 9]|[3, 5, 6, 5, 2, 1, 3, 5]\", \"output\": \"4\"}\n{\"input\": \"[6, 3]|[5, 5]\", \"output\": \"-1\"}\n{\"input\": \"[8]|[9]\", \"output\": \"-1\"}\n{\"input\": \"[7, 1, 0, 6, 0, 3, 6, 2, 8]|[9, 4, 0, 3, 0, 3, 3, 1, 7]\", \"output\": \"2\"}\n{\"input\": \"[6, 6, 8]|[10, 10, 9]\", \"output\": \"-1\"}\n{\"input\": \"[4, 6, 1, 8, 9, 0, 2, 6, 7]|[5, 6, 9, 9, 10, 7, 7, 8, 5]\", \"output\": \"-1\"}\n{\"input\": \"[7, 0, 10, 10]|[10, 1, 8, 10]\", \"output\": \"-1\"}\n{\"input\": \"[3, 3, 1, 0, 6, 4]|[0, 9, 3, 5, 10, 3]\", \"output\": \"-1\"}\n{\"input\": \"[4, 4, 9, 7, 10, 8, 4, 1, 4, 3]|[3, 7, 7, 1, 5, 5, 3, 1, 9, 5]\", \"output\": \"2\"}\n{\"input\": \"[5, 1, 0, 9, 7, 0, 3]|[8, 0, 3, 3, 8, 3, 9]\", \"output\": \"-1\"}\n{\"input\": \"[9, 0]|[9, 6]\", \"output\": \"-1\"}\n{\"input\": \"[5, 1, 6, 9, 2, 0, 6, 9]|[8, 8, 1, 1, 2, 2, 4, 9]\", \"output\": \"2\"}\n{\"input\": \"[4, 2, 7, 1, 6]|[3, 2, 6, 5, 6]\", \"output\": \"-1\"}\n{\"input\": \"[7, 2, 7, 2, 7, 8]|[6, 7, 9, 7, 7, 8]\", \"output\": \"-1\"}\n{\"input\": \"[4, 0, 6, 2, 1]|[6, 9, 3, 3, 9]\", \"output\": \"-1\"}\n{\"input\": \"[10, 4, 1, 5, 5, 6, 9, 10, 2]|[2, 9, 4, 0, 3, 5, 10, 5, 4]\", \"output\": \"0\"}\n{\"input\": \"[9, 5, 2, 8]|[2, 0, 9, 9]\", \"output\": \"0\"}\n{\"input\": \"[6, 2, 0, 10, 1, 4, 5, 6]|[0, 2, 3, 5, 1, 5, 5, 8]\", \"output\": \"0\"}\n{\"input\": \"[5, 10, 8, 3, 8, 10, 10, 10, 8]|[4, 3, 9, 5, 9, 3, 0, 7, 9]\", \"output\": \"0\"}\n{\"input\": \"[0, 8, 2, 7, 0, 2, 5, 7, 2, 5]|[5, 1, 9, 5, 8, 1, 5, 1, 10, 4]\", \"output\": \"-1\"}\n{\"input\": \"[0, 8, 2, 8, 0, 5, 6, 7, 1]|[2, 9, 6, 4, 7, 5, 4, 4, 7]\", \"output\": \"-1\"}\n{\"input\": \"[1, 10, 9, 2]|[1, 0, 2, 2]\", \"output\": \"0\"}\n{\"input\": \"[7, 0, 7]|[3, 2, 4]\", \"output\": \"0\"}\n{\"input\": \"[10, 1, 7, 10, 4, 6]|[0, 7, 2, 4, 0, 5]\", \"output\": \"0\"}\n{\"input\": \"[3, 6, 0, 5, 8]|[7, 8, 5, 1, 6]\", \"output\": \"-1\"}\n{\"input\": \"[6, 1, 9, 8, 1]|[0, 5, 6, 8, 1]\", \"output\": \"0\"}\n{\"input\": \"[10, 0, 10, 1, 7, 6, 8, 9]|[5, 10, 1, 9, 1, 10, 4, 4]\", \"output\": \"2\"}\n{\"input\": \"[2, 1, 3, 3, 10, 5, 10, 0, 2]|[3, 2, 6, 4, 10, 6, 10, 10, 10]\", \"output\": \"-1\"}\n{\"input\": \"[9, 6, 4, 8, 1, 8, 8, 9, 5]|[2, 4, 3, 6, 6, 10, 0, 1, 2]\", \"output\": \"0\"}\n{\"input\": \"[3]|[4]\", \"output\": \"-1\"}\n{\"input\": \"[1, 0]|[9, 8]\", \"output\": \"-1\"}\n{\"input\": \"[8, 0, 0, 10, 0, 10, 5, 6]|[0, 8, 0, 6, 5, 3, 4, 8]\", \"output\": \"5\"}\n{\"input\": \"[0]|[9]\", \"output\": \"-1\"}\n{\"input\": \"[1, 10, 4]|[6, 9, 5]\", \"output\": \"-1\"}\n{\"input\": \"[9, 4]|[2, 0]\", \"output\": \"0\"}\n{\"input\": \"[5, 2, 9, 1, 3, 3, 4]|[5, 2, 10, 7, 2, 5, 2]\", \"output\": \"-1\"}\n{\"input\": \"[6, 0, 3, 0, 4]|[10, 6, 7, 2, 0]\", \"output\": \"-1\"}\n{\"input\": \"[6]|[5]\", \"output\": \"0\"}\n{\"input\": \"[2, 0, 2]|[6, 5, 3]\", \"output\": \"-1\"}\n{\"input\": \"[0, 2, 6, 7, 7, 5, 10, 5, 4, 1]|[2, 5, 7, 8, 2, 9, 0, 9, 10, 9]\", \"output\": \"-1\"}\n{\"input\": \"[1, 8, 5, 8, 4, 8, 8, 3]|[3, 3, 4, 4, 2, 5, 1, 3]\", \"output\": \"1\"}\n{\"input\": \"[0, 6, 0, 0, 5, 0, 4]|[1, 1, 5, 4, 7, 4, 5]\", \"output\": \"-1\"}\n{\"input\": \"[10, 4, 10]|[3, 4, 3]\", \"output\": \"0\"}\n{\"input\": \"[3, 7, 8]|[5, 6, 8]\", \"output\": \"-1\"}\n{\"input\": \"[5, 10, 9]|[4, 2, 5]\", \"output\": \"0\"}\n{\"input\": \"[2, 3]|[10, 8]\", \"output\": \"-1\"}\n{\"input\": \"[6, 7, 5, 2]|[5, 6, 0, 7]\", \"output\": \"0\"}\n{\"input\": \"[4, 7, 1, 1]|[7, 3, 6, 6]\", \"output\": \"-1\"}\n{\"input\": \"[8]|[9]\", \"output\": \"-1\"}\n{\"input\": \"[5, 2, 9, 0, 0, 4, 3, 7]|[4, 0, 3, 10, 0, 2, 7, 5]\", \"output\": \"-1\"}\n{\"input\": \"[8, 5, 1, 7, 3, 8, 1, 4]|[6, 6, 2, 5, 5, 10, 3, 4]\", \"output\": \"-1\"}\n{\"input\": \"[2, 8, 5]|[4, 4, 4]\", \"output\": \"1\"}\n{\"input\": \"[2, 8]|[9, 2]\", \"output\": \"-1\"}\n{\"input\": \"[0, 6, 4, 6, 8, 10]|[5, 10, 3, 5, 3, 4]\", \"output\": \"2\"}\n{\"input\": \"[5, 0, 9, 0, 6, 7, 3, 6, 1, 9]|[4, 2, 4, 8, 8, 2, 5, 9, 9, 9]\", \"output\": \"-1\"}\n{\"input\": \"[0, 1, 4, 7, 3, 6, 9, 5, 7]|[7, 1, 7, 8, 4, 4, 4, 1, 8]\", \"output\": \"-1\"}\n{\"input\": \"[8, 6, 9, 6, 4, 0, 3, 7, 10, 6]|[0, 1, 3, 9, 2, 3, 3, 4, 7, 6]\", \"output\": \"0\"}\n{\"input\": \"[0, 4, 3]|[10, 1, 10]\", \"output\": \"-1\"}\n{\"input\": \"[8, 8, 0, 2, 9, 8, 5, 6, 4, 2]|[1, 1, 8, 2, 3, 4, 9, 4, 0, 6]\", \"output\": \"0\"}\n{\"input\": \"[4, 6]|[7, 1]\", \"output\": \"1\"}\n{\"input\": \"[2, 7, 10, 3, 6, 7]|[2, 0, 9, 0, 5, 3]\", \"output\": \"0\"}\n{\"input\": \"[3, 0]|[10, 5]\", \"output\": \"-1\"}\n{\"input\": \"[8, 6, 0]|[10, 3, 9]\", \"output\": \"-1\"}\n{\"input\": \"[1, 8, 2, 6, 0, 9, 5, 1, 8]|[2, 3, 9, 1, 1, 4, 2, 0, 9]\", \"output\": \"3\"}\n{\"input\": \"[5, 9, 6, 0, 6, 0, 10, 10, 6, 7]|[0, 0, 5, 4, 4, 3, 6, 9, 1, 6]\", \"output\": \"0\"}\n{\"input\": \"[6, 9, 1, 0, 6]|[8, 8, 4, 6, 2]\", \"output\": \"-1\"}\n{\"input\": \"[3, 5, 2, 2, 0, 3, 3]|[3, 0, 8, 3, 0, 8, 3]\", \"output\": \"-1\"}\n{\"input\": \"[7, 7]|[6, 7]\", \"output\": \"0\"}\n{\"input\": \"[3, 6, 10, 9, 3, 0, 2, 3]|[0, 4, 9, 10, 2, 4, 7, 6]\", \"output\": \"-1\"}\n{\"input\": \"[1, 7]|[2, 5]\", \"output\": \"1\"}\n{\"input\": \"[2, 10, 7, 8, 9, 9]|[8, 6, 10, 10, 5, 5]\", \"output\": \"4\"}\n{\"input\": \"[3, 10, 4, 8, 4]|[3, 3, 0, 9, 5]\", \"output\": \"0\"}\n{\"input\": \"[10, 9, 10, 2, 3, 7, 2]|[7, 8, 10, 6, 9, 8, 9]\", \"output\": \"-1\"}\n{\"input\": \"[8, 2, 0, 0, 4]|[0, 6, 1, 1, 8]\", \"output\": \"-1\"}\n{\"input\": \"[8, 8, 4, 0, 1, 2, 1, 9, 8]|[0, 0, 8, 8, 1, 10, 9, 8, 3]\", \"output\": \"-1\"}\n{\"input\": \"[10, 8]|[2, 7]\", \"output\": \"0\"}\n{\"input\": \"[2, 5, 8, 2, 8, 5, 1, 8]|[8, 0, 6, 0, 10, 10, 10, 5]\", \"output\": \"-1\"}\n{\"input\": \"[3, 7, 10, 3, 1]|[9, 10, 2, 6, 1]\", \"output\": \"-1\"}\n{\"input\": \"[7]|[9]\", \"output\": \"-1\"}\n{\"input\": \"[0]|[1]\", \"output\": \"-1\"}\n{\"input\": \"[4, 7, 9, 2, 10]|[3, 1, 7, 1, 7]\", \"output\": \"0\"}\n{\"input\": \"[2, 8, 10, 7, 2, 5]|[8, 10, 6, 10, 5, 3]\", \"output\": \"-1\"}\n{\"input\": \"[5, 8, 2, 8]|[0, 0, 0, 0]\", \"output\": \"0\"}\n{\"input\": \"[10, 10, 2, 4, 10, 10, 0, 3]|[2, 10, 0, 8, 5, 7, 9, 3]\", \"output\": \"0\"}\n{\"input\": \"[10, 4, 6, 7]|[6, 2, 1, 5]\", \"output\": \"0\"}\n{\"input\": \"[7, 1, 0, 7, 6, 2, 0, 1]|[6, 0, 10, 2, 8, 8, 6, 8]\", \"output\": \"-1\"}\n{\"input\": \"[4, 0, 3, 6, 5, 8]|[2, 2, 4, 9, 1, 4]\", \"output\": \"4\"}\n{\"input\": \"[8, 2, 10, 9, 10, 3, 6, 2, 3]|[9, 2, 2, 3, 6, 9, 7, 8, 8]\", \"output\": \"-1\"}\n{\"input\": \"[6, 1, 6, 5, 2, 6, 8, 0]|[5, 7, 2, 3, 6, 10, 10, 2]\", \"output\": \"-1\"}\n{\"input\": \"[8, 1]|[0, 6]\", \"output\": \"0\"}\n{\"input\": \"[10, 10, 5, 6, 7]|[3, 7, 0, 6, 9]\", \"output\": \"0\"}\n{\"input\": \"[10, 10, 10, 0, 9, 9]|[6, 2, 10, 8, 9, 0]\", \"output\": \"0\"}\n{\"input\": \"[6, 3, 10]|[6, 10, 8]\", \"output\": \"-1\"}\n{\"input\": \"[2, 3, 8, 7, 1, 3, 7]|[6, 1, 3, 3, 0, 0, 2]\", \"output\": \"1\"}\n{\"input\": \"[0, 8]|[3, 3]\", \"output\": \"1\"}\n{\"input\": \"[2, 6, 1]|[8, 2, 4]\", \"output\": \"-1\"}\n{\"input\": \"[6]|[9]\", \"output\": \"-1\"}\n{\"input\": \"[6, 6, 2]|[0, 0, 6]\", \"output\": \"0\"}\n{\"input\": \"[10, 4, 4, 4, 0, 3, 10, 10]|[9, 9, 6, 4, 8, 10, 0, 4]\", \"output\": \"-1\"}\n{\"input\": \"[7]|[4]\", \"output\": \"0\"}\n{\"input\": \"[6, 4, 1, 1, 2]|[9, 8, 3, 1, 5]\", \"output\": \"-1\"}\n{\"input\": \"[9, 0, 5, 0, 3, 0]|[8, 0, 9, 2, 5, 7]\", \"output\": \"-1\"}\n{\"input\": \"[4]|[8]\", \"output\": \"-1\"}\n{\"input\": \"[7, 4, 10]|[5, 7, 8]\", \"output\": \"2\"}\n"
        })

        # Execute the code
        response = self.executor.execute(
            code_template=CODE_TEMPLATE,
            solution_code="class Solution:\n    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:\n        n = len(gas)\n        total_gas = 0\n        curr_gas = 0\n        start_index = 0\n\n        for i in range(n):\n            total_gas += gas[i] - cost[i]\n            curr_gas += gas[i] - cost[i]\n\n            if curr_gas < 0:\n                curr_gas = 0\n                start_index = i + 1\n        \n        return start_index if total_gas >= 0 else -1\n            \n\n\n# Naive: iterate through gas, then check costs. if it doesnt work, move to next starting index and continue. O(n^2) time. Can we optimize? to O(n)? extra data structure? ",
            metadata=metadata
        )

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