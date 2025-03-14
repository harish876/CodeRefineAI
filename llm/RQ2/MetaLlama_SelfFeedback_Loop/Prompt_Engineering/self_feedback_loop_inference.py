import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
from transformers import AutoConfig

config = AutoConfig.from_pretrained("meta-llama/Llama-3.2-1B")
print(config)


# Authenticate with Hugging Face
HF_TOKEN = "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"  # Replace with your actual token
login(token=HF_TOKEN)

# Load LLaMA 1.3B Instruct model

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")
# Load model with correct rope_scaling format
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-1B",
    rope_scaling={"type": "linear", "factor": 32.0}  # Ensure correct format
)

# Enable MPS (Apple Silicon Acceleration)
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
model = model.to(device)

def optimize_code(problem, code):
    prompt = f"### Task: Optimize the following Python code to improve efficiency and make it more concise. Do not explain or use comments, only return the optimized code. Give a code according to Python 3.8 and the whole answer should be enclosed in a Class Solution and function name should be the same as submitted to you in the input code\n\n#### Input Code:\n{code}\n\n#### Optimized Code:\n"

    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(device)


        # Generate optimized code
    outputs = model.generate(**inputs, max_new_tokens=500, temperature=0.7, top_p=0.9)

        # Decode generated text
    optimized_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
    optimized_code = optimized_code.split("#### Optimized Code:")[-1].strip()
        # Extract the part after "#### Optimized Code:"
    return optimized_code


# Load dataset
with open("dataset/balanced_samples.json", "r") as file:
    dataset = json.load(file)

# Process first 200 samples
optimized_results = []
for sample in dataset[:200]:
    if not sample["runtime_inefficient_codes"]:  # Skip if the list is empty
        continue
    

    question_prompt = sample["prompt"]
    first_runtime_code = sample["runtime_inefficient_codes"][0]["code"]
    
    optimized_code = optimize_code(question_prompt, first_runtime_code)
    optimized_results.append({
        "questionId": sample["question_id"],
        "llm_generated_code": optimized_code,
        "import_code": sample["import_code"],
        "setup_code": sample["setup_code"],
        "entry_point": sample["entry_point"],
        "difficulty": sample["difficulty"]
    })

# Save optimized results to a JSON file
with open("dataset/balanced_samples.json", "w") as output_file:
    json.dump(optimized_results, output_file, indent=4)

print("Optimized code has been saved to optimized_code_results.json")
