from transformers import GPTNeoXForCausalLM, AutoTokenizer


import json
 
from tqdm import tqdm 

import torch

from call_llm_inference import inference, init_llm_model 
 
def _gen_prompt(question,solution):
    instruction_template=f"Given the question '{question}' and one solution '{solution}', check whether the solution is efficient or not. Write 'Yes' if it is correct, and 'No' if it is not"
    return instruction_template
 
def check_accuracy(response_dict):
    correct=0
    incorrect=0
    for question_id in response_dict:
        judgement_for_efficient_code=response_dict[question_id]["runtime_efficient_codes"]["judgement"]
        judgement_for_inefficient_code=response_dict[question_id]["runtime_inefficient_codes"]["judgement"]
        if "yes" in judgement_for_efficient_code.lower() and "no" in judgement_for_inefficient_code.lower():
            incorrect+=1
        elif "yes" in judgement_for_efficient_code.lower():
            correct+=1
        else:
            incorrect+=1
        if "yes" in judgement_for_efficient_code.lower() and "no" in judgement_for_inefficient_code.lower():
            incorrect+=1
        elif "no" in judgement_for_inefficient_code.lower():
            correct+=1
        else:
            incorrect+=1
    return correct/(correct+incorrect),correct,correct+incorrect
 
def judge_efficiency():
    with open('data/new_dataset.json') as f:
        conceptnet_json_list = json.load(f)
    response_dict={}
    tokenizer, sampling_params, llm = init_llm_model()  
    for i,conceptnet_json in enumerate(tqdm(conceptnet_json_list)):
        question=conceptnet_json["prompt"]
        question_id=conceptnet_json["question_id"]
        efficient_solution=conceptnet_json["runtime_efficient_codes"][0]["code"]
        inefficient_solution=conceptnet_json["runtime_inefficient_codes"][0]["code"]
        if question_id not in response_dict:
            response_dict[question_id]={"runtime_efficient_codes":{},"runtime_inefficient_codes":{}}
        
        prompt  = _gen_prompt(question,efficient_solution)
        judgement_for_efficient_code=inference(tokenizer, sampling_params, llm,prompt)
        prompt  = _gen_prompt(question,inefficient_solution)
        judgement_for_inefficient_code=inference(tokenizer, sampling_params, llm,prompt)
        response_dict[question_id]["runtime_efficient_codes"]={"judgement":judgement_for_efficient_code}
        response_dict[question_id]["runtime_inefficient_codes"]={"judgement":judgement_for_inefficient_code}
        if i>50:
            break #FIXME
        
    with open(f'judgement.json', 'w') as fp:
        json.dump(response_dict, fp, indent=4)
    accuracy,correct,total=check_accuracy(response_dict)
    print(accuracy,correct,total)
  
 
        
        

if __name__ == '__main__':
    judge_efficiency()