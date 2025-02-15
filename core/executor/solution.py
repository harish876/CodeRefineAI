#TODO: Enable this to choose code for different use cases, like memory,runtime inefficient,moderate etc...
import pandas as pd
import json

from_file = True

def get_solution(question_id: int, row: pd.Series = None) -> str:
    if from_file:
        with open("/Users/harishgokul/CodeRefineAI/dataset/optimized_test_results_meta.json", "r") as file:
            optimized_data = json.load(file)
            
        solution_code = None
        for record in optimized_data:
            if question_id == record["question_id"]:
                solution_code = record["optimized_code"]
                break
        
        return solution_code
        
    else:
        solution_code = row['runtime_efficient_codes']
        if not solution_code:
            print("Runtime efficient solution not available")
            return None
        
        return solution_code[0]["code"]