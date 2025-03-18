
import json 
import copy 
from tqdm import tqdm 
from tqdm import tqdm 
import random 
import torch



def sample_solution():
    with open('dataset/balanced_samples.json') as f:
        conceptnet_json_list = json.load(f)
    result=[]
    
    for i,conceptnet_json in enumerate(tqdm(conceptnet_json_list)):
        new_conceptnet_json=copy.deepcopy(conceptnet_json)
        if "runtime_efficient_codes" in conceptnet_json and "runtime_inefficient_codes" in conceptnet_json and len(conceptnet_json["runtime_efficient_codes"])>0 and len(conceptnet_json["runtime_inefficient_codes"])>0:
            runtime_efficient_solutions=conceptnet_json["runtime_efficient_codes"]
            sampled_runtime_efficient_solution=random.choice(runtime_efficient_solutions)
            runtime_inefficient_solutions=conceptnet_json["runtime_inefficient_codes"]
            sampled_runtime_inefficient_solution=random.choice(runtime_inefficient_solutions)
            new_conceptnet_json["runtime_efficient_codes"]=[sampled_runtime_efficient_solution]
            new_conceptnet_json["runtime_inefficient_codes"]=[sampled_runtime_inefficient_solution] 
        if "memory_inefficient_codes" in conceptnet_json and "memory_efficient_codes" in conceptnet_json and len(conceptnet_json["memory_efficient_codes"])>0 and len(conceptnet_json["memory_inefficient_codes"])>0:
            memory_efficient_solutions=conceptnet_json["memory_efficient_codes"]
            sampled_memory_efficient_solution=random.choice(memory_efficient_solutions)
            memory_inefficient_solutions=conceptnet_json["memory_inefficient_codes"]
            sampled_memory_inefficient_solution=random.choice(memory_inefficient_solutions)
            new_conceptnet_json["memory_inefficient_codes"]=[sampled_memory_inefficient_solution]
            new_conceptnet_json["memory_efficient_codes"]=[sampled_memory_efficient_solution] 
        
        result.append(new_conceptnet_json)
        

        
    with open(f'dataset/balanced_samples_w_one_solution_per_type.json', 'w') as fp:
        json.dump(result, fp, indent=4)

sample_solution()