from typing import List

from core.executor.config import Settings, load_settings
from core.executor.executor import Executor, ExecutorResponse
import pandas as pd
from src.solution import SolutionMetric, SolutionType, get_solution
from core.executor.utils.template import *
import json
import os
import argparse

def submit(executor: Executor, source_file: str, result_file: str, solution_metadata: dict[str,any]):
    df = pd.read_json(source_file)

    submissions: List[ExecutorResponse] = []
    for _, row in df.iterrows():
        id = row["question_id"]
        solution_metric = SolutionMetric[solution_metadata["solution_metric"].upper()]
        solution_type = SolutionType[solution_metadata["solution_type"].upper()]
        solution, error = get_solution(
            question_id=id,
            data_file_path=solution_metadata["solution_file"],
            solution_metric=solution_metric,
            solution_type=solution_type,
            row=row
        )
        if solution is None:
            print(f"Error at question_id {id}.No solution found")
            continue

        if error is not None:
            print(f"Error at question_id {id} {error}.")
            continue

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
        if not saved_submission.get('token',None):
            continue
        
        submission_details = executor.get_submission_details(submission_id=saved_submission['token'])
        saved_submission['submission_details'] = submission_details.json()
        
    with open(result_file, "w") as outfile:
        json.dump(saved_submissions, outfile, indent=4)
    
    print("Submission results saved successfully")

def main():
    data_dir = "/Users/harishgokul/CodeRefineAI/dataset"
    settings = load_settings("/Users/harishgokul/CodeRefineAI/.env")
    
    parser = argparse.ArgumentParser(description="Submit or get results from Judge0")
    parser.add_argument("action", choices=["submit", "get"], help="Action to perform")
    parser.add_argument("--file", help="Source file containing dataset. Do not add the extension", default="dataset_preview")
    parser.add_argument("--dir", help="Base directory to fetch files from", default=data_dir)
    parser.add_argument("--solution_file", help="Source file containing Solution dataset. Solutions from LLM's", default=None)
    parser.add_argument("--solution_metric", help = "Solution metric if the row is passed in [runtime,memory]", default="runtime")
    parser.add_argument("--solution_type", help = "Solution type if the row is passed in [efficient,inefficient,moderate]", default="efficient")
    args = parser.parse_args()

    
    executor = Executor(settings=settings)
    
    if args.dir:
        data_dir = args.dir
    
    file_name = args.file
    source_file = os.path.join(data_dir, f"{file_name}.json")
    result_file = os.path.join(data_dir, f"{file_name}_submissions.json")
    solution_file = os.path.join(data_dir, f"{args.solution_file}.json") if args.solution_file else None
    
    if not os.path.exists(source_file):
        print(f"Source file does not exist {source_file}")
        
    if not os.path.exists(result_file):
        print(f"Result file does not exist {result_file}. Creating file....")
        with open(result_file, "w") as f:
            json.dump([], f)
        
    print("Args ================================")
    print(f"Data Directory: {data_dir}")
    print(f"Source File: {source_file}")
    print(f"Result File: {result_file}")
    print(f"Solution File: {solution_file}")
    print("================================")
    
    if args.action == "submit":
        submit(executor, source_file, result_file, {
            "solution_file": solution_file,
            "solution_metric": args.solution_metric,
            "solution_type": args.solution_type
        })
    elif args.action == "get":
        get_results(executor, result_file)

if __name__ == "__main__":
    main()