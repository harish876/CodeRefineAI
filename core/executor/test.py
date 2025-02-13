import json
import sys

from typing import List
import random

# Define necessary data structures
class Solution:
    def candy(self, ratings: List[int]) -> int:
        return Solution().compute_candy(ratings)

    def compute_candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        left = [1] * n
        right = [1] * n
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                left[i] = left[i - 1] + 1
            else:
                left[i] = 1

        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                right[i] = right[i + 1] + 1
            else:
                right[i] = 1

        ans = 0
        for i in range(n):
            ans += max(left[i], right[i])
        return ans

# Test case generator
class TestCaseGenerator:
    def generate(self) -> dict:
        # Example Test Case
        test_case_1 = {'ratings': [1, 0, 2]}
        test_case_2 = {'ratings': [1, 2, 2]}
        # Additional Test Cases
        test_case_3 = {'ratings': [3, 2, 1]}
        test_case_4 = {'ratings': [1, 3, 4, 5, 2]}
        test_case_5 = {'ratings': [1, 2, 87, 87, 87, 2, 1]}
        return random.choice([test_case_1, test_case_2, test_case_3, test_case_4, test_case_5])

    def encode_input(self, input_obj) -> str:
        return str(input_obj)

    def encode_output(self, output_obj) -> str:
        return str(output_obj)

    def decode_input(self, input_str) -> dict:
        return eval(input_str)

class Runner:
    def __init__(self, solution: Solution):
        self.solution: Solution = solution
        self.test = TestCaseGenerator()
    
    def run(self):
        test_cases = json.loads(sys.stdin.read().strip())

        for test_case in test_cases:
            decoded_input = self.test.decode_input(test_case['input'])
            expected_output = test_case['output']
            
            output = self.solution.candy(decoded_input)
            actual_output = self.test.encode_output(output)
            
            if actual_output != expected_output:
                print("Input", decoded_input)
                print("Expected Output: ", expected_output)
                print("Actual Output: ", actual_output)
                print("Test Failed!")
                return
        
        print("Test Passed!")

if __name__ == "__main__":
    solution = Solution()
    runner = Runner(solution)
    runner.run()