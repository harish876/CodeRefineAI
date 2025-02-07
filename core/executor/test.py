import sys
from collections import defaultdict

class Solution:
    def isValid(self, s: str) -> bool:
        st = []
        mp = defaultdict(str, {']': '[', '}': '{', ')': '('})

        for char in s:
            if st and st[-1] == mp.get(char):
                st.pop()
            else:
                st.append(char)
        
        return len(st) == 0


class Runner:
    def __init__(self, solution: Solution):
        self.solution = solution
    
    def run(self):
        test_cases = sys.stdin.read().strip().split("\n")
        
        results = [("true" if self.solution.isValid(tc) else "false") for tc in test_cases]
        
        print("\n".join(results))


if __name__ == "__main__":
    solution = Solution()
    runner = Runner(solution)
    runner.run()