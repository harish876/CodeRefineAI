import json
from coderefineai_executor import Settings, Executor
import pandas as pd
from coderefineai_executor import Executor

# Load the optimized_results.json file
with open("llm/RQ2/MetaLlama_SelfFeedback_Loop/Output_Results/output_samples.json", "r") as file:
    data = json.load(file)

# Initialize Executor settings
settings = Settings(
    env="dev",
    self_hosted=True,
    judge0_base_url="http://64.23.144.74:2358",
    judge0_api_key="",
    num_runs=3
)

executor = Executor(settings)

# Iterate through the list and execute the llm_generated_code
for item in data:
    solution_code = item.get("llm_generated_code")

    metadata = pd.Series({
               "question_id": item.get("questionId"),
                "name": item.get("name"),
                "setup_code": item.get("setup_code"),
                "entry_point": item.get("entry_point"),
                "import_code": item.get("import_code"),
                "test_cases": item.get("testcases")
            }) 

    if solution_code and not metadata.empty:
        print(f"Executing code for item: {item.get('id', 'Unknown')}")
        try:
            response = executor.execute(
                               solution_code=solution_code,
                               metadata=metadata
            )
            print("Execution Response:", response)

            submission = executor.get_submission_details(submission_id=response.token)
           

            # Polls for until response is Accepted or there is a runtime error
            submission = executor.poll_submission_status(submission_id=response.token)
            submission_details = submission.json()
            item["runtime"] = submission_details.get("time")
            item["status"] = submission_details.get("status", {}).get("description", "Unknown Status")

        except Exception as e:
            print(f"Error during execution: {e}")
            item["runtime"] = None
            item["status"] = "Execution Failed"

    else:
        print("Skipping item due to missing solution_code or metadata.")


# Save optimized results to a JSON file
with open("llm/RQ2/MetaLlama_SelfFeedback_Loop/Output_Results/executed_optimized_results.json", "w") as output_file:
    json.dump(data, output_file, indent=4)
