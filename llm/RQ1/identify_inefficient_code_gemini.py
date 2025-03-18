from transformers import GPTNeoXForCausalLM, AutoTokenizer

#CUDA_VISIBLE_DEVICES=4,5 PYTHONPATH=.  python llm/identify_inefficient_code.py
import json
 
from tqdm import tqdm 
import random 
import torch

from call_llm_inference_gemini import inference_gemini, init_llm_model_gemini 
 
def _gen_prompt(question,solution,efficient_type):
    instruction_template=f"Given the question '{question}' and one solution '{solution}', check whether the solution is efficient or not with respect to {efficient_type}. Write 'Yes' if it is correct, and 'No' if it is not. No need to explain the code. Only output 'Yes' or 'No'"
    return instruction_template
 
def check_accuracy(response_dict,efficiency_type):
    correct=0
    incorrect=0
    for question_id in response_dict:
        
        efficient_code_name=f"{efficiency_type}_efficient_codes"
        inefficient_code_name=f"{efficiency_type}_inefficient_codes"
        
        if efficient_code_name in response_dict[question_id] and inefficient_code_name in response_dict[question_id]:
            judgement_for_efficient_code=response_dict[question_id][efficient_code_name]["judgement"]
            judgement_for_inefficient_code=response_dict[question_id][inefficient_code_name]["judgement"]
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
 

def compare_one_type(conceptnet_json,efficient_type,response_dict,question_id,question,tokenizer, sampling_params, llm,model_name) :
    efficient_code_key=f"{efficient_type}_efficient_codes"
    inefficient_code_key=f"{efficient_type}_inefficient_codes"
    if efficient_code_key in conceptnet_json and inefficient_code_key in conceptnet_json and len(conceptnet_json[efficient_code_key])>0 and len(conceptnet_json[inefficient_code_key])>0:
        efficient_solution=conceptnet_json[efficient_code_key][0]["code"]
        inefficient_solution=conceptnet_json[inefficient_code_key][0]["code"]
        if question_id not in response_dict:
            response_dict[question_id]={efficient_code_key:{},inefficient_code_key:{}}
        else:
            response_dict[question_id].update({efficient_code_key:{},inefficient_code_key:{}})
        prompt  = _gen_prompt(question,efficient_solution,efficient_type)
        judgement_for_efficient_code=inference_gemini(tokenizer, sampling_params, llm,prompt,model_name)
        prompt  = _gen_prompt(question, inefficient_solution,efficient_type)
        judgement_for_inefficient_code=inference_gemini(tokenizer, sampling_params, llm,prompt,model_name)
        response_dict[question_id][efficient_code_key]={"judgement":judgement_for_efficient_code}
        response_dict[question_id][inefficient_code_key]={"judgement":judgement_for_inefficient_code}
    return response_dict
 
def judge_efficiency(model_name,model_post_fix):
    with open('dataset/balanced_samples_w_one_solution_per_type.json') as f:
        conceptnet_json_list = json.load(f)
    response_dict={}
    tokenizer, sampling_params, llm = init_llm_model_gemini(model_name)  
    for i,conceptnet_json in enumerate(tqdm(conceptnet_json_list)):
        question=conceptnet_json["prompt"]
        question_id=conceptnet_json["question_id"]
        
        efficient_type="runtime"
        response_dict=compare_one_type(conceptnet_json,efficient_type,response_dict,question_id,question,tokenizer, sampling_params, llm,model_name) 
        efficient_type="memory"
        response_dict=compare_one_type(conceptnet_json,efficient_type,response_dict,question_id,question,tokenizer, sampling_params, llm,model_name) 
        with open(f'judgement_samples_200_{model_post_fix}.json', 'w') as fp:
            json.dump(response_dict, fp, indent=4)
    accuracy,correct,total=check_accuracy(response_dict,"runtime")
    print(accuracy,correct,total)
    #save accuracy in file
    with open(f'accuracy_llama_{model_post_fix}.txt', 'w') as f:
        f.write(f'{accuracy} {correct} {total}')
    print(f'{accuracy} {correct} {total}')
  
 
        
        

if __name__ == '__main__':
    model_name="gemini-2.0-flash"
    model_post_fix=model_name.replace("/","_")
    print(f"use model {model_name}")
    judge_efficiency(model_name,model_post_fix)