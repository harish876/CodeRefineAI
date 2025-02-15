import json
import sys
import collections

from typing import Optional

# Necessary DS declarations for different problems
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        arr = collections.defaultdict(Node)
        cur = head
        if not head:
            return None

        while cur:
            arr[cur] = Node(cur.val, None, None)
            cur = cur.next
        
        cur = head
        while cur:
            if cur.random:
                arr[cur].random = arr[cur.random]
            if cur.next:
                arr[cur].next = arr[cur.next]
            cur = cur.next
        return arr[head]

class TestCaseGenerator:

    def generate(self) -> dict:
        nodes = [{'val': 7, 'random_index': None}, {'val': 13, 'random_index': 0}, {'val': 11, 'random_index': 4}, {'val': 10, 'random_index': 2}, {'val': 1, 'random_index': 0}]
        head = self.build_linked_list(nodes)
        return {'head': head}

    def build_linked_list(self, node_info):
        if not node_info:
            return None
        nodes = [Node(info['val']) for info in node_info]
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        for i, info in enumerate(node_info):
            if info['random_index'] is not None:
                nodes[i].random = nodes[info['random_index']]
        return nodes[0]

    def encode_input(self, input_obj) -> str:
        return str(self.linked_list_to_array(input_obj['head']))

    def encode_output(self, output_obj) -> str:
        if not output_obj:
            return str([])
        return str(self.linked_list_to_array(output_obj))

    def decode_input(self, input_str) -> dict:
        data = eval(input_str)
        return {'head': self.build_linked_list(data)}

    def linked_list_to_array(self, head: 'Node') -> list:
        if not head:
            return []
        nodes = []
        current = head
        while current:
            random_index = None
            if current.random is not None:
                random_index = self.find_index(head, current.random)
            nodes.append({'val': current.val, 'random_index': random_index})
            current = current.next
        return nodes

    def find_index(self, head: 'Node', node: 'Node') -> int:
        current, index = (head, 0)
        while current:
            if current == node:
                return index
            current = current.next
            index += 1
        return -1

class Runner:
    def __init__(self, solution: Solution):
        self.solution: Solution = solution
        self.test = TestCaseGenerator()
    
    def run(self):
        test_cases = json.loads(sys.stdin.read().strip())

        for test_case in test_cases:
            input = self.test.decode_input(test_case['input'])
            expected_output = test_case['output']
            
            output = self.solution.copyRandomList(**input)
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