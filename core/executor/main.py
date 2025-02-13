from typing import List
from core.executor.config import Settings
from core.executor.executor import Executor, ExecutorResponse
import pandas as pd
from core.executor.solution import get_solution
from core.utils.template import *
import json
import os
import time
import argparse

def submit(executor: Executor, source_file: str, result_file: str):
    df = pd.read_json(source_file)
        
    submissions: List[ExecutorResponse] = []
    for _, row in df.iterrows():
        solution = get_solution(row)
        result = executor.execute(
            code_template=template,
            solution_code=solution,
            metadata=row
        )  
        submissions.append(result)      
    
    with open(result_file, "w") as outfile:
        json.dump([submission.model_dump() for submission in submissions], outfile, indent=4)
    
    print("Submission calls made successfully")

def get_results(executor: Executor, result_file: str):
    with open(result_file, "r") as infile:
        saved_submissions = json.load(infile)
    
    for saved_submission in saved_submissions:
        submission_details = executor.get_submission_details(submission_id=saved_submission['token'])
        saved_submission['submission_details'] = submission_details.json()
        
    with open(result_file, "w") as outfile:
        json.dump(saved_submissions, outfile, indent=4)
    
    print("Submission results saved successfully")

def main():
    data_dir = "/Users/harishgokul/CodeRefineAI/dataset"
    settings = Settings()
    
    parser = argparse.ArgumentParser(description="Submit or get results from Judge0")
    parser.add_argument("action", choices=["submit", "get"], help="Action to perform")
    parser.add_argument("--file", help="Source file containing dataset. Do not add the extension", default="dataset_preview")
    parser.add_argument("--dir", help="Base directory to fetch files from", default=data_dir)
    args = parser.parse_args()

    
    executor = Executor(settings=settings)
    
    if args.dir:
        data_dir = args.dir
    
    file_name = args.file
    source_file = os.path.join(data_dir, f"{file_name}.json")
    result_file = os.path.join(data_dir, f"{file_name}_submissions.json")
    
    if not os.path.exists(source_file):
        print(f"Source file does not exist {source_file}")
        
    if not os.path.exists(result_file):
        print(f"Result file does not exist {result_file}. Creating file....")
        with open(result_file, "w") as f:
            json.dump([], f)
        
    print("Config: ")
    print(f"Data Directory: {data_dir}")
    print(f"Source File: {source_file}")
    print(f"Result File: {result_file}")
    
    if args.action == "submit":
        submit(executor, source_file, result_file)
    elif args.action == "get":
        get_results(executor, result_file)

if __name__ == "__main__":
    main()