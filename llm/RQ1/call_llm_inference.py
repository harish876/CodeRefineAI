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

def init_llm_model(model_name="Qwen/Qwen2.5-Coder-1.5B-Instruct"):
    
    # Initialize the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Pass the default decoding hyperparameters of Qwen2.5-7B-Instruct
    # max_tokens is for the maximum length for generation.
    

    # Input the model name or path. Can be GPTQ or AWQ models.
    llm = LLM(model=model_name,max_num_seqs=100) # ,gpu_memory_utilization=0.3 ,tensor_parallel_size=2
    
    sampling_params = llm.get_default_sampling_params()
    sampling_params.max_tokens=512
        # sampling_params = SamplingParams(temperature=0.7, top_p=0.8, repetition_penalty=1.05, )
  
    return tokenizer, sampling_params, llm

def inference(tokenizer, sampling_params, llm,prompt,model_name):
    # Prepare your prompts
  
    messages = [
        {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # generate outputs
    outputs = llm.generate([text], sampling_params,use_tqdm=False)

    # Print the outputs.
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        # print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
    
        
        
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
    tokenizer, sampling_params, llm = init_llm_model()  
    inference(tokenizer, sampling_params, llm,prompt)
    
def test_inference_answer():
    prefix = "What is one way a dog can contribute to home security?"
    expected_answer="dog can guard your house"
    prediction="What is one way a dog can contribute to home security?\n\nA dog can help you keep your home safe by alerting you to intruders."
    prompt=f"For the question '{prefix}', the answer is '{expected_answer}' while the model generated the following question: '{prediction}'. Could you judge whether the model prediction aligns with the expected answer? Provide your judgement as 'yes' or 'no' without other words."
    tokenizer, sampling_params, llm = init_llm_model()  
    generated_text=inference(tokenizer, sampling_params, llm,prompt)
    print(generated_text)
    #Yes. The model's prediction aligns with the expected answer. Both indicate that a dog can contribute to home security by acting as a guard or by alerting the owner to intruders.
    
if __name__ == '__main__': 
    test_inference_answer()