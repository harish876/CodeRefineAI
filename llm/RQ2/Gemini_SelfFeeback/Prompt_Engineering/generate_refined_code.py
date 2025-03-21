import json
import time
import google.generativeai as genai



with open("llm/RQ2/Gemini_SelfFeeback/Output_Results/Second_Refinement_Results/executed_refinement2_with_feedback.json", "r") as f:
    dataset = json.load(f)

# ✅ Replace with your actual API Key
GEMINI_API_KEY = "AIzaSyBVQ38Dc-R6Y5jH3omvSu9KOLNT2EQKztw"
# Initialize Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


# Function to process and generate optimized code
def generate_refined_code():
    api_calls = 0  # Track API call count

    for sample in dataset[:200]:
        # Get the first inefficient code
        qid = sample["questionId"]
        runtime = sample["runtime"]
        code = sample["llm_generated_code"]
        feedback = sample["feedback"]
        # Create prompt
        prompt = f"### Task: Optimize the following Python code to improve efficiency considering the feedback and execution time and make it more concise. Do not explain or use comments, only return the optimized code. Give a code according to Python 3.8 and the whole answer should be enclosed in a Class Solution and function name should be the same as submitted to you in the input code #### Input Code:\n{code} #### Feedback:\n{feedback} #### Execution time:\n{runtime} \n\n#### Optimized Code:\n"

        try:
            # Generate content using Gemini API
            response = model.generate_content(prompt)

            # Extract generated content
            generated_code = response.candidates[0].content.parts[0].text if response.candidates else None

            if generated_code:
                generated_code = generated_code.split("```python")[-1].split("```")[0].strip()
                generated_code = generated_code.split("#### Optimized Code:")[-1].strip()
                sample["llm_generated_code"] = generated_code
                print(f"Successfully optimized code {generated_code} for iteration {api_calls}")
            else:
                print(f"⚠️ Warning: Empty response for question_id {qid}")

        except Exception as e:
            print(f"Error processing question_id {qid}: {e}")
            continue  # Skip this question and proceed

        # Increment API call counter
        api_calls += 1

        # Sleep after every 14 API calls to avoid exhaustion
        if api_calls % 14 == 0:
            print("⏳ API limit reached. Sleeping for 60 seconds...")
            time.sleep(60)

    return dataset

# Run the function
optimized_results = generate_refined_code()

# Save the results
with open("llm/RQ2/Gemini_SelfFeeback/Output_Results/Third_Refinement_Results/output_samples_refinement3.json", "w") as f:
    json.dump(optimized_results, f, indent=4)

print("🎉 Optimized code has been saved to optimized_codes.json")
