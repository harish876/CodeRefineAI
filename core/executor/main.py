from textwrap import indent
from typing import List
from requests import Response
from core.executor.config import Settings
from core.executor.executor import Executor
import json
import pandas as pd
import os
from core.utils.template import *

def main():
    settings = Settings()
    data_file = "/Users/harishgokul/CodeRefineAI/dataset/dataset_preview.json"
    df = pd.read_json(data_file)
        
    executor = Executor(settings = settings)
    submissions = []
    template = static_tc_template
    for _,row in df.iterrows():
        if row["question_id"] != 131:
            continue
        
        entry_point = row['entry_point']
        raw_source_code = template.format(
           entry_point=entry_point,
           import_code=row["import_code"],
           setup_code=row["setup_code"],
        )
        print(raw_source_code)
        test_cases = json.dumps(row['test_cases'])
        result:Response= executor.submit(
                        raw_source_code=raw_source_code, 
                        test_cases=test_cases, 
                        expected_results="Test Passed!"
                    )
        
        submission_id = result.json()["token"]
        submissions.append({
            "question_id": row["question_id"],
            "title": row["name"],
            "token":submission_id
        })
    
    print("Submissions: ",submissions)
    
    # for submission_id in submissions:
    #     submission_details = executor.get_submission_details(submission_id)
    #     print("Submission Details: ", submission_details.json())
        
if __name__ == "__main__":
    main()