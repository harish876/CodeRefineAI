import base64
import ast
from html.parser import HTMLParser
import re

def extract_class(source_code: str, class_name: str) -> str:
    tree = ast.parse(source_code)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return ast.unparse(node)  

    return None  

def extract_python_code(text):
    code_blocks = re.findall(r"```py(.*?)```", text, re.DOTALL)
    return "\n\n".join(code_blocks).strip()
def encode_base64(text: str) -> str:
    encoded_bytes = base64.b64encode(text.encode("utf-8"))
    return encoded_bytes.decode("utf-8")

def decode_base64(encoded_text: str) -> str:
    decoded_bytes = base64.b64decode(encoded_text.encode("utf-8"))
    return decoded_bytes.decode("utf-8")


template = """
import json
import itertools
import collections
import heapq
import bisect
import string
import sys
import functools
import math
import copy
import re
# import numpy as np
# import pandas as pd

from math import floor, ceil, factorial, sqrt, inf
from sys import maxsize, stdin
from bisect import bisect_left, bisect_right
from itertools import permutations, zip_longest
from heapq import heappush, heappop, heapify
from collections import deque, defaultdict, OrderedDict, Counter
from typing import List, Optional, Tuple
from functools import lru_cache
# from sortedcontainers import SortedList

{import_code}

### LC DATA STRUCTURES START ###
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
### LC DATA STRUCTURES END ###

{solution_code}

{test_case_code}

class Runner:
    def __init__(self, solution: Solution):
        self.solution: Solution = solution
        self.test = TestCaseGenerator()
        self.num_tests = 10 # Change dynamically
    
    def run(self):
        test_cases = json.loads(sys.stdin.read().strip())

        for i in range(min(self.num_tests,len(test_cases))):
            test_case = test_cases[i]
            input = self.test.decode_input(test_case['input'])
            expected_output = test_case['output']
            
            output = self.solution.{entry_point}(**input)
            actual_output = self.test.encode_output(output)
            
            if actual_output != expected_output:
                print("Input", input)
                print("Expected Output: ", expected_output)
                print("Actual Output: ", actual_output)
                print(f"{{i+1}} Test Failed!")
                return
        
        #print metadata to stderr
        print("Tests Passed!")

if __name__ == "__main__":
    solution = Solution()
    runner = Runner(solution)
    runner.run()
"""
