import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

HUGGINGFACE_TOKEN = "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"


MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HUGGINGFACE_TOKEN)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype=torch.float16, device_map="auto", token=HUGGINGFACE_TOKEN
)


# Function to run inference
def run_deepseek(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")  # Move to GPU
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=1024)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Function to process a single question
def process_question(question):
    question_id = question["question_id"]
    name = question["name"]
    
    # Select the most memory-inefficient code (highest runtime)
    memory_inefficient_code = max(question["runtime_inefficient_codes"], key=lambda x: x["runtime"])

    # Step 1: Optimize Code
    coder_prompt = f"Optimize the Python program below to be functionally equivalent but run faster and use less memory:\n\n{memory_inefficient_code['code']}\n\nOptimized version:"
    optimized_code = run_deepseek(coder_prompt)

    # Step 2: Get Feedback
    feedback_prompt = f"Give feedback in English for why the code solution below is incorrect or inefficient and how the program can be fixed:\n\n{optimized_code}\n\nFeedback:"
    feedback = run_deepseek(feedback_prompt)

    # Step 3: Refine Code
    refine_prompt = f"Refine the given incorrect or sub-optimal code solution based on the feedback specified below:\n\nFeedback:\n{feedback}\n\nRefined Code:"
    refined_code = run_deepseek(refine_prompt)

    # Return results for this question
    return {
        "question_id": question_id,
        "name": name,
        "original_code": memory_inefficient_code["code"],
        "optimized_code": optimized_code,
        "feedback": feedback,
        "refined_code": refined_code
    }


def main():
    # Load dataset
    with open('/mnt/data/dataset_preview.json', 'r') as f:
        dataset = json.load(f)

    results = []
    
    # Process each question
    for question in dataset:
        print(f"Processing Question ID: {question['question_id']} - {question['name']}")
        result = process_question(question)
        results.append(result)

    # Save results to a JSON file
    output_path = "/mnt/data/deepseek_results_inefficient.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"\n✅ All questions processed. Results saved to {output_path}")

# Run the script
if __name__ == "__main__":
    main()
