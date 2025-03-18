from transformers import AutoTokenizer
from vllm import LLM, SamplingParams
import os 
os.environ["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn"
os.environ["LIBRARY_PATH"] =  "/usr/local/cuda/lib64/stubs"
from google import genai
import time


from llm.key import google_api_key
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    after_log
) 

@retry(wait=wait_random_exponential(min=1, max=120), stop=stop_after_attempt(3))#, after=after_log(logger, logging.INFO)
def chat_completions_with_backoff(llm,prompt):
    try:
        output=llm.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
    except Exception as e:
        print(e)
        raise e 
    return output

def init_llm_model_gemini(model_name="Qwen/Qwen2.5-Coder-1.5B-Instruct"):
   
   
    llm = genai.Client(api_key=google_api_key)
    tokenizer, sampling_params=None,None 
    return tokenizer, sampling_params, llm

def inference_gemini(tokenizer, sampling_params, llm,prompt,model_name):
    # Prepare your prompts
     
    response = chat_completions_with_backoff(llm,prompt)
    generated_text=response.text
    #generate code to sleep
    time.sleep(20)
        
        
    return generated_text
 
 

def batch_inference(tokenizer, sampling_params, llm,prompts ):
    # Prepare your prompts
    text_list=[]
    for prompt in prompts:
        messages = [
            {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        text_list.append(text)

    # generate outputs
    outputs = llm.generate(text_list, sampling_params,use_tqdm=True)
    generated_text_list=[]
    # Print the outputs.
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        generated_text_list.append(generated_text)
        # print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
    return generated_text_list 
 
def test_inference():
    prompt = "What is the capital of France?"
    tokenizer, sampling_params, llm = init_llm_model_gemini()  
    inference_gemini(tokenizer, sampling_params, llm,prompt)
    
def test_inference_answer():
    prefix = "What is one way a dog can contribute to home security?"
    expected_answer="dog can guard your house"
    prediction="What is one way a dog can contribute to home security?\n\nA dog can help you keep your home safe by alerting you to intruders."
    prompt=f"For the question '{prefix}', the answer is '{expected_answer}' while the model generated the following question: '{prediction}'. Could you judge whether the model prediction aligns with the expected answer? Provide your judgement as 'yes' or 'no' without other words."
    tokenizer, sampling_params, llm = init_llm_model_gemini()  
    generated_text=inference_gemini(tokenizer, sampling_params, llm,prompt)
    print(generated_text)
    #Yes. The model's prediction aligns with the expected answer. Both indicate that a dog can contribute to home security by acting as a guard or by alerting the owner to intruders.
    
if __name__ == '__main__': 
    test_inference_answer()