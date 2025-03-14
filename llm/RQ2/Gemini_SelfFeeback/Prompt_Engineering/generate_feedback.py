import json
import time
import google.generativeai as genai



with open("llm/RQ2/Gemini_SelfFeeback/Output_Results/First_Pass_Output/executed_first_pass.json", "r") as f:
    dataset = json.load(f)

# ✅ Replace with your actual API Key
GEMINI_API_KEY = "AIzaSyDL_hqHaSfT2NPDZz5XXnBboJz3Piio7MY"
# Initialize Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


# Function to process and generate optimized code
def generate_feedback():
    api_calls = 0  # Track API call count

    for sample in dataset:
        if "llm_generated_code" not in sample or not sample["llm_generated_code"]:
            print(f"Skipping question_id {qid} (missing or empty 'llm_generated_code')")
            continue

        runtime = sample["runtime"]
        code = sample["llm_generated_code"]
        status = sample["status"]
        # Create prompt
        prompt = f"Give feedback in english in atmost 150 characters for why the code solution below is incorrect or having a runtime error or inefficient and how the program can be fixed.Don't generate the corrected code just tell the reasoning.## Candidate solution:{code}##Result when executed:{status}##Runtime:{runtime}## Feedback for incorrectness/inefficiency and how it can be improved:"

        try:
            # Generate content using Gemini API
            response = model.generate_content(prompt)

            # Extract generated content
            feedback = response.candidates[0].content.parts[0].text if response.candidates else None

            if feedback:
                feedback = feedback.split("## Feedback for incorrectness/inefficiency and how it can be improved:")[-1].strip()
                sample["feedback"] = feedback
                print(f"Successfully generated feedback: {feedback} for iteration {api_calls}")
            else:
                print(f"⚠️ Warning: Empty response for question_id {qid}")

        except Exception as e:
            print(f"Error processing question_id {qid}: {e}")
            continue  # Skip this question and proceed

        # Increment API call counter
        api_calls += 1

        # Sleep after every 14 API calls to avoid exhaustion
        if api_calls % 14 == 0:
            print("API limit reached. Sleeping for 60 seconds...")
            time.sleep(60)

    return dataset

# Run the function
optimized_results = generate_feedback()

# Save the results
with open("llm/RQ2/Gemini_SelfFeeback/Output_Results/First_Pass_Output/executed_first_pass_with_feedback.json", "w") as f:
    json.dump(optimized_results, f, indent=4)
