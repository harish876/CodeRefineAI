from typing import List
from unittest import result

from coderefineai_executor import Executor,Settings,ExecutorResponse,CODE_TEMPLATE
import pandas as pd
from solution import SolutionMetric, SolutionType, get_solution
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
    data_dir = "/Users/harishgokul/CodeRefineAI/dataset/P2" #changing this for P2.
    settings = Settings(
        env="dev",
        self_hosted=True,
        judge0_base_url="http://64.23.144.74:2358",
        judge0_api_key="",
    )
    
    parser = argparse.ArgumentParser(description="Submit or get results from Judge0")
    parser.add_argument("action", choices=["submit", "get"], help="Action to perform")
    parser.add_argument("model", choices=["gemini", "llama"], help="Model used to perform the experiment")
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
    model_name = args.model
    source_file = os.path.join(data_dir, f"{file_name}.json")
    
    if args.solution_file is not None:
        result_file = os.path.join(data_dir, f"{file_name}_{model_name}_codegen_submissions.json")
    else:
        result_file = os.path.join(data_dir, f"{file_name}_{model_name}_reference_submissions.json")
        
    solution_file = os.path.join(data_dir, f"{args.solution_file}.json") if args.solution_file else None
    
    if not os.path.exists(source_file):
        print(f"Source file does not exist {source_file}")
        
    if not os.path.exists(result_file):
        print(f"Result file does not exist {result_file}. Creating file....")
        with open(result_file, "w") as f:
            json.dump([], f)
        
    print("Args ================================")
    print(f"Data Directory: {data_dir}")
    print(f"Model: {model_name}")
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