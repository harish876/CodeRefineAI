import json
import time
import pandas as pd
from pydantic import BaseModel
import requests
from .utils import extract_class
from .utils import encode_base64
from typing import Optional
from requests import Response
from .config import Settings


class ExecutorResponse(BaseModel):
    status: str
    question_id: Optional[int] = None
    title: Optional[str] = None
    token: Optional[str] = None
    error: Optional[str] = None 
    code: Optional[str] = None
        
        
class Executor():
    def __init__(self, settings: Settings):
        self._config = settings
        self._querystring = {"base64_encoded": "true", "wait": "false", "fields": "*"}
        if settings.self_hosted:
            self._headers = {}
        else:
            self._headers = {
                "x-rapidapi-key": self._config.judge0_api_key,
                "x-rapidapi-host": "judge0-extra-ce.p.rapidapi.com",
                "Content-Type": "application/json"
            }
        self._default_language_id = self._get_language_id("python")
    
    def _get_language_id(self, language: str):
        match language.lower():
            case "python":
                return 71 if self._config.self_hosted else 28
            case _:
                raise ValueError("Unsupported language")
    
   
    def _submit(self,
                raw_source_code: str,
                test_cases: str, 
                expected_results: str,
                language: Optional[str] = "python", 
                ) -> requests.Response:
        
        """
            Submits the provided source code and test cases to the Judge0 API for execution and validation.
            Args:
                raw_source_code (str): The source code to be executed.
                test_cases (str): The input test cases for the source code.
                expected_results (str): The expected output results for the test cases.
                language (Optional[str], optional): The programming language of the source code. Defaults to "python".
            Returns:
                requests.Response: The response from the Judge0 API containing the submission results.
            Raises:
                Exception: If the submission fails or the response status code is not 201.
                requests.exceptions.RequestException: If there is an error during the request.
        """
        
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
    
    def get_submission_details(self, submission_id: str):
        """
        Retrieves the details of a submission from the Judge0 API.
        Args:
            submission_id (str): The ID of the submission to retrieve.
        Returns:
            response: The response object containing the submission details if the request is successful.
        Raises:
            Exception: If the submission cannot be retrieved or if the response status code is not 200.
            requests.exceptions.RequestException: If there is an error during the request.
        """
        try:
            url = f"{self._config.judge0_base_url}/submissions/{submission_id}"
            response = requests.get(url, headers=self._headers)
              
            if response.status_code == 200:
                return response
            else:
                raise Exception(f"Unable to retrieve submission with {submission_id}", response)
        
        except requests.exceptions.RequestException as e:
            raise f"Error retrieving submission: {e}"
        
    def poll_submission_status(self, submission_id: str, max_retries: int = 5, initial_delay: int = 1) -> Response:
        """
        Polls the submission status with exponential backoff until a final status is reached.

        Args:
            submission_id (str): The ID of the submission to poll.
            max_retries (int): The maximum number of retries. Defaults to 5.
            initial_delay (int): The initial delay between retries in seconds. Defaults to 1.

        Returns:
            Response: The response object containing the final submission details.

        Raises:
            TimeoutError: If the maximum number of retries is exceeded.
        """
        retries = 0
        delay = initial_delay

        while retries < max_retries:
            submission_details = self.get_submission_details(submission_id)
            status = submission_details.json().get("status", {}).get("description")

            if status in ["Accepted", "Wrong Answer", "Compilation Error", "Runtime Error (NZEC)", "Time Limit Exceeded"]:
                return submission_details

            print(f"Status: {status}. Retrying in {delay} seconds...")
            time.sleep(delay)
            retries += 1
            delay *= 2  # Exponential backoff

        raise TimeoutError("Max retries exceeded while polling submission status.")
    
    def execute(self, code_template: str, solution_code: Optional[str], metadata: pd.Series) -> ExecutorResponse:
        """
        Executes the provided code template with the given solution code and metadata.

        Parameters:
        - code_template (str): The template of the code to be executed.
        - solution_code (Optional[str]): The solution code to be inserted into the template.
        - metadata (pd.Series): A pandas Series containing metadata required for execution, including:
            - 'setup_code' (str): The setup code required for execution.
            - 'question_id' (str): The ID of the question.
            - 'name' (str): The name/title of the question.
            - 'entry_point' (str): The entry point function or method.
            - 'import_code' (str): The import statements required for execution.
            - 'test_cases' (list): A list of test cases to be executed.

        Returns:
        - ExecutorResponse: An object containing the status of the execution, question ID, title, token, and optionally the raw source code or error message.

        Raises:
        - KeyError: If required metadata keys are missing.
        """
        
        setup_code = metadata.get('setup_code', None)
        if not setup_code:
            return ExecutorResponse(
                status="failure",
                question_id=metadata["question_id"],
                title=metadata["name"],
                token=None,
                error="No Setup code found",
            )

        test_case_code = extract_class(setup_code, "TestCaseGenerator")
        if not test_case_code:
            return ExecutorResponse(
                status="failure",
                question_id=metadata["question_id"],
                title=metadata["name"],
                token=None,
                error="No test case decoder found",
            )

        if not solution_code:
            return ExecutorResponse(
                status="failure",
                question_id=metadata["question_id"],
                title=metadata["name"],
                token=None,
                error="No solution found",
            )

        entry_point = metadata['entry_point']
        import_code = metadata['import_code']
        raw_source_code = code_template.format(
            entry_point=entry_point,
            import_code=import_code,
            solution_code=solution_code,
            test_case_code=test_case_code,
        )
        test_cases = json.dumps(metadata['test_cases'])
        result: Response = self._submit(
            raw_source_code=raw_source_code, 
            test_cases=test_cases, 
            expected_results="Tests Passed!"
        )

        submission_id = result.json()["token"]
        return ExecutorResponse(
            status="success",
            question_id=metadata["question_id"],
            title=metadata["name"],
            token=submission_id,
            code=raw_source_code
        )
    
    def execute_code(self, code: str, test_cases: str, expected_results: str) -> ExecutorResponse:
        """
        Executes the given code with the provided test cases and expected results.

        Args:
            code (str): The source code to be executed.
            test_cases (str): The test cases to run against the source code.
            expected_results (str): The expected results for the test cases.

        Returns:
            ExecutorResponse: An object containing the status of the execution, 
                      the submission token, and the original code.
        """
        
        result: Response = self._submit(
            raw_source_code=code, 
            test_cases=test_cases, 
            expected_results=expected_results
        )

        submission_id = result.json()["token"]
        return ExecutorResponse(
            status="success",
            question_id=None,
            title=None,
            token=submission_id,
            code=code
        )