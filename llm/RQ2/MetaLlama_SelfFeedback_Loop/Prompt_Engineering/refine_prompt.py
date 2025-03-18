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

def generate_feedback(status, code, runtime):
    prompt = f"### Task: Optimize the following Python code to improve efficiency considering the feedback and execution time and make it more concise. Do not explain or use comments, only return the optimized code. Give a code according to Python 3.8 and the whole answer should be enclosed in a Class Solution and function name should be the same as submitted to you in the input code #### Input Code:\n{code} #### Feedback:\n{feedback} #### Execution time:\n{runtime} \n\n#### Optimized Code:\n"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    try:
        # Generate optimized code
        outputs = model.generate(**inputs, max_length=1024, max_new_tokens=500, temperature=0.7, top_p=0.9)

        # Decode generated text
        feedback = tokenizer.decode(outputs[0], skip_special_tokens=True)

        feedback = feedback.split("## Feedback for incorrectness/inefficiency and how it can be improved:")[-1].strip()
        print(feedback)
        # Extract the part after "#### Optimized Code:"
        return feedback

    except Exception as e:
        print(f"Error optimizing code: {e}")
        return None


# Load dataset
with open("llm/RQ2/MetaLlama_SelfFeedback_Loop/Output_Results/output_samples_with_feedback.json", "r") as file:
    dataset = json.load(file)

for sample in dataset:
    if not sample["llm_generated_code"]:  # Skip if the list is empty
        continue


    runtime = sample["runtime"]
    llm_generated_code = sample["llm_generated_code"]
    status = sample["status"]

    feedback = generate_feedback(status, llm_generated_code, runtime)

    sample["feedback"]=feedback


# Save optimized results to a JSON file
with open("llm/RQ2/MetaLlama_SelfFeedback_Loop/Output_Results/output_samples_with_feedback.json", "w") as output_file:
    json.dump(data, output_file, indent=4)

