from transformers import GPTNeoXForCausalLM, AutoTokenizer


import json
 
from tqdm import tqdm 

import torch

from call_llm_inference import inference, init_llm_model 
 
def _gen_prompt(question,solution):
    instruction_template=f"Given the question '{question}' and one solution '{solution}', check whether the solution is efficient or not." 
    return instruction_template
 
def judge_efficiency():
 
    
    with open('dataset.json') as f:
        conceptnet_json_list = json.load(f)
    response_dict={}
    tokenizer, sampling_params, llm = init_llm_model()  
    for conceptnet_json in conceptnet_json_list:
        question=conceptnet_json["promt"]
        efficient_solution=conceptnet_json["runtime_efficient_codes"][0]["code"]
        inefficient_solution=conceptnet_json["runtime_inefficient_codes"][0]["code"]
        if question not in response_dict:
            response_dict[question]={}
        if efficient_solution not in response_dict[question]:
            response_dict[question][efficient_solution]={}
        if inefficient_solution not in response_dict[question]:
            response_dict[question][inefficient_solution]={}
        prompt  = _gen_prompt(question,efficient_solution)
        judgement_for_efficient_code=inference(tokenizer, sampling_params, llm,prompt)
        prompt  = _gen_prompt(question,inefficient_solution)
        judgement_for_inefficient_code=inference(tokenizer, sampling_params, llm,prompt)
        response_dict[question][efficient_solution]={"judgement":judgement_for_efficient_code}
        response_dict[question][inefficient_solution]={"judgement":judgement_for_inefficient_code}
        with open(f'judgement.json', 'w') as fp:
            json.dump(response_dict, fp, indent=4)
  
 
        
        

if __name__ == '__main__':
    judge_efficiency()