import enum
import os
from attr import dataclass
import pandas as pd
import json
from typing import  Optional, Tuple

@dataclass
class SolutionMetric(enum.Enum):
    RUNTIME = "runtime"
    MEMORY = "memory"
    
@dataclass
class SolutionType(enum.Enum):
    EFFICIENT = "efficient"
    INEFFICIENT = "inefficient"
    MODERATE = "moderate"


def get_solution_mapping(solution_metric: SolutionMetric,solution_type: SolutionType):
    return f"{solution_metric.value}_{solution_type.value}_codes"
    

def get_solution(
    question_id: int, 
    data_file_path: Optional[str],
    solution_metric: SolutionMetric = SolutionMetric.RUNTIME,
    solution_type: SolutionType = SolutionType.EFFICIENT,
    row: Optional[pd.Series] = None
    ) -> Tuple[Optional[str],Optional[str]]:
    
    
    if data_file_path is not None:
        if not os.path.exists(data_file_path):
            return (None,"Solution File not found")
        
        with open(data_file_path, "r") as file:
            optimized_data = json.load(file)
            
        solution_code = None
        for record in optimized_data:
            if question_id == record["question_id"]:
                solution_code = record["optimized_code"]
                break
        
        return (solution_code,None)
        
    else:
        field = get_solution_mapping(solution_metric,solution_type)
        solution_code = row[field]
        if not solution_code:
            return (None,f"{field.replace('_', ' ').capitalize()} solution not available in dataset")
        
        if len(solution_code) == 0:
            return (None,f"Solution for {field.value} not available in dataset. Length is 0")
            
        #TODO: sort as per the runtime or memory
        return (solution_code[0]["code"],None)
    