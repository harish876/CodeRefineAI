import argparse
import os
from smolagents.agents import CodeAgent, fix_final_answer_code
from smolagents import PythonInterpreterTool
from llm_sandbox import SandboxSession
from smolagents import tool, LiteLLMModel
from typing import List, Optional, Tuple
from bs4 import BeautifulSoup
import json
import pandas as pd

from core.executor.config import Settings


def format_prompt_to_ascii(prompt: str):
    parser = BeautifulSoup(prompt,features="lxml")
    ascii_text = parser.get_text()
    return ascii_text

def run_tool(prompt: str):
    settings = Settings()

    model = LiteLLMModel(model_id="gemini/gemini-2.0-flash-exp",api_key=settings.google_gemini_api_key)
    # litellm._turn_on_debug()

    @tool
    def run_code(lang: str, code: str, libraries: Optional[List] = None) -> Tuple[str, str]:
        """
        Executes the given code in the specified language.Run code in a sandboxed environment.

        Args:
            lang: The language of the code.
            code: The code to run.
            libraries: The libraries to use. Defaults to None.
        
        Returns:
            Tuple[str, str]: A tuple containing:
                - code (str): The code used to provide the output.
                - output (str): The output of the executed code.
        """
        with SandboxSession(lang=lang, verbose=False) as session:  # type: ignore[attr-defined]
            return session.run(code, libraries).text
        
    agent = CodeAgent(tools=[run_code],model=model)
    output = agent.run(format_prompt_to_ascii(prompt))
    return output
    
 
def main():
    data_dir = "/Users/harishgokul/CodeRefineAI/dataset"
    parser = argparse.ArgumentParser(description="Submit or get results from Judge0")
    parser.add_argument("question_id", help="Question Id")
    parser.add_argument("--file", help="Source file containing dataset. Do not add the extension", default="dataset_preview")
    parser.add_argument("--dir", help="Base directory to fetch files from", default=data_dir)
    args = parser.parse_args()
    
    if args.dir:
        data_dir = args.dir
    
    file_name = args.file
    source_file = os.path.join(data_dir, f"{file_name}.json")
    result_file = os.path.join(data_dir, f"{file_name}_tool_submissions.json")
    
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
    print("================================")
    
    df = pd.read_json(source_file)
    if 'question_id' not in df.columns:
        print("The dataframe does not contain a 'question_id' field.")
        return
        
    filtered_df = df[df['question_id'] == int(args.question_id)]
        
    if filtered_df.empty:
        print(f"No entries found for question_id {args.question_id}")
        return
    
    prompt = filtered_df["prompt"].values[0]
    print(f"Executing Prompt: {prompt}...")
    
    output = run_tool(prompt)
    print("Output from the agent: {}".format(fix_final_answer_code(str(output))))
    new_entry = {
        "question_id": int(args.question_id),
        "prompt": prompt,
        "output": "{}".format(output),
    }
    
    with open(result_file, "w") as f:
        json.dump([new_entry], f, indent=4)
    
    print(f"Results updated to {result_file}")
    
if __name__ == "__main__":
    main()

    