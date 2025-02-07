import pydantic
from requests import Response
from core.executor.config import Settings
from core.executor.executor import Executor

import os

def main():
    try:
        settings = Settings()
        with open(f"{os.getcwd()}/test.py","r") as file:
            raw_source_code = file.read()
            
        executor = Executor(settings = settings)
        
        test_cases = '\n'.join(["()","()[]","(()())","[{()}]","({[}])"]) #Assume we get test cases newline separated
        expected_results = '\n'.join(["true","true","true","true","false"]) # Same format for expected results
        
        
        result:Response= executor.submit(
                        raw_source_code=raw_source_code, 
                        test_cases=test_cases, 
                        expected_results=expected_results
                    )
        
        submission_id = result.json()["token"]
        print("Submission ID: ",submission_id)
        
        submission_details = executor.get_submission_details(submission_id)
        print("Submission Details: ", submission_details.json())
        
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
if __name__ == "__main__":
    main()