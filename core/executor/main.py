import pydantic
from requests import Response
from core.executor.config import Settings
from core.executor.executor import Executor

def main():
    try:
        settings = Settings()
        with open("/Users/harishgokul/CodeRefineAI/core/executor/test.py","r") as file:
            raw_source_code = file.read()
            
        executor = Executor(settings = settings)
        
        test_cases = '\n'.join(["()","()[]","(()())","[{()}]","({[}])"])
        expected_results = '\n'.join(["true","true","true","true","false"])
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