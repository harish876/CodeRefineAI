# CodeRefineAI
**Title** : Can LLM's identify and remove Software Inefficiencies?
1. [Research Question 1](#Research-Question-1): How accurately LLMs can detect and reason code inefficiencies on LLM? 
2. [Research Question 2](#Research-Question-2): How can we use different prompt engineering techniques on LLM models to produce efficient code? 
3. [Research Question 3](#Research-Question-3): Which LLM model and model settings are suitable to generate the most efficient code?

# Dataset
## Dataset Description

The balanced_samples dataset contains 200 programming problems from LeetCode, with multiple reference implementations for each problem including:
- Runtime efficient solutions
- Runtime inefficient solutions 
- Memory efficient solutions
- Memory inefficient solutions

Each problem is categorized by difficulty level (Easy, Medium, Hard) and annotated with relevant programming topics (e.g., Dynamic Programming, Arrays, Graphs).

This balanced collection ensures comprehensive testing across different algorithmic concepts, complexity levels, and inefficiency patterns, providing a robust benchmark for evaluating LLM capabilities in code optimization.

Dataset has been augmented to categorise the solutions into the category mentioned above . Here is the link to the dataset and the script used for augmentation.

-   Original Dataset  - [Venus_t] (https://huggingface.co/datasets/Elfsong/Venus_t)
-   Augumented Dataset - [Dataset](/dataset/balanced_samples.json)
-   Augmentation Script - [Processing Script](/dataset/processing_dataset.ipynb)


# Tools Used
## Code Executor Utility
- [CodeRefineAI Executor](https://pypi.org/project/coderefineai-executor/): Custom Pip package which provides code submission, submission status polling, parametrising number of runs, utility to switch between self hosted/ cloud offering with a code template for formatting leetcode styles problems.
- [Instruction on usage](/coderefineai_executor/README.md)
- [Demo on how to use this package](/src/reference.ipynb)


## Code Submission Utility

### Overview
This utility script provides a command-line interface for submitting code solutions to a Judge0 execution environment and retrieving the results. It is designed to work with both reference solutions and LLM-generated code (Gemini or Llama).

### Installation

### Usage
The script supports two primary operations:

1. Submitting code solutions for execution
2. Retrieving results of previously submitted solutions

### Command Format

### Parameters
| Parameter           | Description                                    | Required | Default               |
|--------------------|--------------------------------|----------|----------------------|
| `action`           | Either "submit" or "get"               | ✓        | -                    |
| `model`            | Either "gemini" or "llama"              | ✓        | -                    |
| `--file`           | Source dataset filename (without extension)  |          | "dataset_preview"   |
| `--dir`            | Base directory for files                     |          | Current P2 directory |
| `--solution_file`  | File containing LLM solutions                 |          | None                 |
| `--solution_metric`| Metric to evaluate (runtime/memory)          |          | "runtime"           |
| `--solution_type`  | Solution type (efficient/inefficient/moderate) |          | "efficient"         |

### Examples

### Help Command
```bash
python src/main.py --help
```


### Submit Reference Solutions
```bash
python src/main.py --action submit gemini --file my_dataset --solution_type efficient --solution_metric runtime
```

### Submit LLM Generated Solutions
```bash
python src/main.py --action submit llama --file my_dataset --solution_file ref_solutions.py
```

### Retrieve Results
```bash
python src/main.py --action get gemini --model gemini --file my_dataset
```

### Output Files
The script generates JSON output files with the following naming conventions:

- For LLM solutions: `{file_name}_{model_name}_codegen_submissions.json`
- For reference solutions: `{file_name}_{model_name}_reference_{metric_type}_submissions.json`

Where `metric_type` will be one of:
- `rt_eff`
- `rt_ineff`
- `mem_eff`
- `mem_ineff`

## Requirements
- Python 3.7+
- Access to a Judge0 instance (self-hosted or cloud)
- The `coderefineai_executor` package

### Notes
- The script requires properly formatted input files with question IDs.
- Each submission gets a token for tracking and later result retrieval.
- Configure the Judge0 instance in the settings section of the script.


# Research Question 1 
## Dataset
- Dataset for Prompting:
    - **Script to sample one solution per efficiency type** : [RQ1_data](/llm/RQ1/sample_one_set_solution_per_problem.py)
## Methodolgy
- **Prompting** :
    - **Purpose**: Trigger LLMs to evaluate whether the given code is efficient or not.
    -  **Gemini Script** - [Gemini_Prompting](/llm/RQ1/identify_inefficient_code_gemini.py) 
    -  **Llama Script** -[Llama_Prompting](/llm/RQ1/identify_inefficient_code.py)
- **Analysis**: 
    - **Description**: Obtain the accuracy of LLMs in identifying inefficient code.
    - **Gemini Script**: [Gemini_accuracy](/llm/RQ1/compute_accuracy_gemini.py)
    - **Llama Script**: [LLaMA_accuracy](/llm/RQ1/compute_accuracy.py)

# Research Question 2
## Dataset
- Dataset for Vanilla Prompting:
    - Code Generated by Gemini : [Gemini](/dataset/P1/balanced_samples_gemini_codegen_submissions.json)
    - Code Generated by LLama 1B : [Llama](/dataset/P2/balanced_samples_gemini_codegen_submissions.json)
    - Reference Solution with Runtime Efficient Solution: [Runtime Efficient Solution](/dataset/P1/balanced_samples_reference_rt_eff_submissions.json)
    - Reference Solution with Runtime Inefficient Solution:[Runtime Inefficient Solution](/dataset/P1/balanced_samples_reference_rt_ineff_submissions.json)
    
## Methodolgy
- **Vanilla Prompting**
    - **Description**: Direct single-shot prompting that provides the LLM with only the problem statement and asks for an optimized solution.
    -   **Implementation**: The model receives the problem description and is asked to generate a solution with a focus on efficiency, without additional guidance or context.
    - **Purpose**: Establishes a baseline for how well LLMs can generate efficient code with minimal intervention.
    -  **Gemini Vanilla Prompting Script** - [Gemini_Vanilla_Prompting](/llm/RQ2/Vanilla%20Prompting/Gemini_vanilla_prompting.ipynb) 
    -  **Llama Vanilla Prompting Script** -[Llama_Vanilla_Prompting](/llm/RQ2/Vanilla%20Prompting/Vanilla%20prompting.ipynb)

- **Reasoning Prompting** : 
    - **Description**: A multi-stage prompting approach that leverages explicit reasoning about algorithmic efficiency before code generation.
    - **Implementation**:
        -   For Gemini: Implements a self-feedback loop where the model first reasons about optimal algorithmic approaches, time/space complexity considerations, and potential inefficiencies before generating the final solution.
        -   For Llama: Uses Gemini as a reasoning engine to generate efficiency insights, which are then distilled and provided to Llama as context for its code generation.
    -   **Purpose**: Tests whether explicit reasoning about algorithmic efficiency improves the quality of generated solutions compared to vanilla prompting.
    -   **Technical Details**: This approach simulates a human developer's thought process by explicitly considering algorithmic trade-offs before implementation.
    -  **Gemini Reasoning Prompting Script** - [Gemini_Vanilla_Prompting](/llm/RQ2/Reasoning_Based_Prompting/Reasoning_based_prompting_Gemini.ipynb) 
    -  **Llama Gemini Reasoning Script** -[Llama_Vanilla_Prompting](/llm/RQ2/Reasoning_Based_Prompting/Reasoning_Based_prompting_MetaLlama..ipynb) 

- **Analysis**: 
    - **Description**: Obtain the results from [final_results.ipynb](/dataset/processing_dataset.ipynb). Sections for RQ2 and RQ3 are labelled in the notebook and can be found under the outlines section.
    - **Results file**: [/dataset/final_result.ipynb](/dataset/final_result.ipynb)


# Research Question 3
- **Analysis**: 
    - **Description**: Obtain the results from [final_results.ipynb](/dataset/processing_dataset.ipynb). Sections for RQ2 and RQ3 are labelled in the notebook and can be found under the outlines section.
    - **Results file**: [/dataset/final_result.ipynb](/dataset/final_result.ipynb)


## Contact
For any questions or inquiries, please contact the very handsome harish876.