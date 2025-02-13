#TODO: Enable this to choose code for different use cases, like memory,runtime inefficient,moderate etc...
import pandas as pd


def get_solution(row: pd.Series) -> str:
    solution_code = row['runtime_efficient_codes']
    if not solution_code:
        print("Runtime efficient solution not available")
        return None
    
    return solution_code[0]["code"]