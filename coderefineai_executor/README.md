# CodeRefineAI
Can LLM's identify and remove Software Inefficiencies?


## Overview

CodeRefineAI is a project aimed at leveraging Large Language Models (LLMs) to identify and remove software inefficiencies. The project includes a code execution framework that allows for the submission and validation of code snippets using the Judge0 API.

## Features

- **Code Execution**: Submit and execute code snippets using the Judge0 API.
- **Template-Based Execution**: Execute code using predefined templates.
- **Direct Code Execution**: Execute entire code snippets directly without templates.
- **Submission Details**: Retrieve detailed information about code submissions.

## Installation

To install the CodeRefineAI package, follow these steps:

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/CodeRefineAI.git
    cd CodeRefineAI
    ```

2. Install the package:

    ```sh
    pip install .
    ```

## Usage

### Example: Template-Based Execution

```python
from coderefineai_executor import Executor,load_settings

# Example settings
settings = load_settings("/path/to/your/.env")

# Create an instance of Executor
executor = Executor(settings)

# Example metadata
metadata = pd.Series({
    "question_id": 1,
    "name": "Example Question",
    "setup_code": "class TestCaseGenerator: ...",
    "entry_point": "main",
    "import_code": "import sys",
    "test_cases": "..." #problem dependent
})

# Execute the code
response = executor.execute(
    code_template="def {entry_point}():\n    {import_code}\n    {solution_code}\n    {test_case_code}",
    solution_code="print('Hello, world!')",
    metadata=metadata
)

print(response)
```


### Example: Direct Code Execution
```python
from coderefineai_executor import Executor,load_settings

# Example settings
settings = Settings(
    env="dev",
    self_hosted=True,
    judge0_base_url="http://64.23.144.74:2358",
    judge0_api_key="",
)

executor = Executor(settings)

# Execute the code
response = executor.execute_code(
    code="print('Hello, world!')",
    test_cases="",
    expected_results="Hello, world!",
    )

    # Print the response for debugging purposes
print(response)
```

### Configuration
The `Settings` class is used to configure the Executor. Here is an example configuration:

```python
from core.executor.config import Settings

settings = Settings(
    env="dev",
    self_hosted=True,
    judge0_base_url="http://64.23.144.74:2358",
    judge0_api_key="",
)
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact
For any questions or inquiries, please contact the very handsome harish876.