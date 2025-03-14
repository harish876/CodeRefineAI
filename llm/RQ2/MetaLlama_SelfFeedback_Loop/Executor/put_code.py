import json

# Load dataset_preview.json
dataset_preview_path = "dataset/balanced_samples.json"
optimized_results_path = "dataset/output_samples.json"

with open(dataset_preview_path, "r") as file:
    dataset_preview = json.load(file)

# Load optimized_results.json
with open(optimized_results_path, "r") as file:
    optimized_results = json.load(file)

# Create a dictionary for quick lookup by question_id
dataset_dict = {item["question_id"]: item for item in dataset_preview}

# Update optimized_results with test cases
for result in optimized_results:
    question_id = result["questionId"]
    if question_id in dataset_dict:
        result["testcases"] = dataset_dict[question_id].get("test_cases", [])
        result["runtime_efficient_codes"] = dataset_dict[question_id].get("runtime_efficient_codes", [])
        result["name"] = dataset_dict[question_id].get("name")
        result["topics"] = dataset_dict[question_id].get("topics", [])
        result["libraries"] = dataset_dict[question_id].get("libraries", [])
        result["prompt"] = dataset_dict[question_id].get("prompt")

# Save the updated optimized_results.json
output_path = "dataset/optimized_results_updated.json"
with open(output_path, "w") as file:
    json.dump(optimized_results, file, indent=4)

print(f"Updated file saved at: {output_path}")
