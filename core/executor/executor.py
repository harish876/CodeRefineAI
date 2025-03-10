import json
import pandas as pd
from pydantic import BaseModel
import requests
from core.utils.ast import extract_class
from core.utils.base64 import encode_base64
from typing import List, Optional
from requests import Response
from core.executor.config import Settings


class ExecutorResponse(BaseModel):
    status: str
    question_id: int
    title: str
    token: Optional[str] = None
    error: Optional[str] = None 
    code: Optional[str] = None
        
        
class Executor():
    def __init__(self,settings: Settings):
        self._config = settings
        self._querystring = {"base64_encoded":"true","wait":"false","fields":"*"}
        if settings.self_hosted:
            self._headers = {}
        else:
            self._headers = {
                "x-rapidapi-key": self._config.judge0_api_key,
                "x-rapidapi-host": "judge0-extra-ce.p.rapidapi.com",
                "Content-Type": "application/json"
            }
        self._default_language_id = self.__get_language_id__("python")
    
    
    def __get_language_id__(self, language: str):
        #Replace with API call here
        match language.lower():
            case "python":
                return 71 if self._config.self_hosted else 28
            case _:
                raise ValueError("Unsupported language")
        
    
    def submit(self,
               raw_source_code: str,
               test_cases:str, 
               expected_results: str,
               language: Optional[str] = "python", 
            ) -> requests.Response:
        
        url = f"{self._config.judge0_base_url}/submissions"
        
        payload = {
            "language_id": self._default_language_id,
            "stdin": encode_base64(test_cases),
            "source_code": encode_base64(raw_source_code),
            "expected_output": encode_base64(expected_results),
            "number_of_runs": self._config.num_runs
        }
                
        try:
            response = requests.post(url, 
                                    json=payload, 
                                    headers=self._headers, 
                                    params=self._querystring)
            
            if response.status_code == 201:
                return response
            else:
                print(response)
                raise Exception("Unable to submit code", response)
        
        except requests.exceptions.RequestException as e:
            raise f"Error submitting code: {e}"
    
    def get_submission_details(self,submission_id: str):
        try:
            url = f"{self._config.judge0_base_url}/submissions/{submission_id}"
            response = requests.get(url, headers=self._headers)
              
            if response.status_code == 200:
                return response
            else:
                raise Exception(f"Unable to retrive submission with {submission_id}", response)
        
        except requests.exceptions.RequestException as e:
            raise f"Error submitting code: {e}"
        
    def execute(self,code_template: str,solution_code:Optional[str],metadata: pd.Series) -> ExecutorResponse:
        setup_code = metadata.get('setup_code', None)
        if not setup_code :
            return ExecutorResponse(
                status="failure",
                question_id=metadata["question_id"],
                title=metadata["name"],
                token=None,
                error="No Setup code found",
            )
            
        test_case_code = extract_class(setup_code, "TestCaseGenerator")
        if not test_case_code :
            return ExecutorResponse(
                status="failure",
                question_id=metadata["question_id"],
                title=metadata["name"],
                token=None,
                error="No test case decoder found",
            )
            
        if not solution_code :
            return ExecutorResponse(
                status =  "failure",
                question_id =   metadata["question_id"],
                title =  metadata["name"],
                token =  None,
                error =  "No solution found",
            )
         
        entry_point = metadata['entry_point']
        import_code = metadata['import_code']
        raw_source_code =code_template.format(
            entry_point=entry_point,
            import_code=import_code,
            solution_code = solution_code,
            test_case_code=test_case_code,
        )
        test_cases = json.dumps(metadata['test_cases'])
        result:Response=self.submit(
                        raw_source_code=raw_source_code, 
                        test_cases=test_cases, 
                        expected_results="Tests Passed!"
                )
            
        submission_id = result.json()["token"]
        return ExecutorResponse(
            status =  "success",
            question_id =  metadata["question_id"],
            title =  metadata["name"],
            token = submission_id,
            code = raw_source_code
        )
 