static_tc_template = """
import json
import sys

{import_code}

{setup_code}

class Runner:
    def __init__(self, solution: Solution):
        self.solution: Solution = solution
        self.test = TestCaseGenerator()
    
    def run(self):
        test_cases = json.loads(sys.stdin.read().strip())

        for test_case in test_cases:
            input = test_case['input']
            expected_output = test_case['output']
            
            output = self.solution.{entry_point}(input)
            actual_output = self.test.encode_output(output)
            
            if actual_output != expected_output:
                print("Input", input)
                print("Expected Output: ", expected_output)
                print("Actual Output: ", actual_output)
                print("Test Failed!")
                return
        
        print("Test Passed!")

if __name__ == "__main__":
    solution = Solution()
    runner = Runner(solution)
    runner.run()
"""


dyn_tc_template = """
import json
import sys

{import_code}

{setup_code}

class Runner:
    def __init__(self, solution: Solution):
        self.solution: Solution = solution
        self.test = TestCaseGenerator()
    
    def run(self):
        test_cases = json.loads(sys.stdin.read().strip())

        for test_case in test_cases:
            decoded_input = self.test.decode_input(test_case['input'])
            expected_output = test_case['output']
            
            output = self.solution.{entry_point}(decoded_input)
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
"""