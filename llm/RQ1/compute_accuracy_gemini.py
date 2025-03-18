

import json 


from llm.identify_inefficient_code_gemini import check_accuracy


def compute(input_path):
    with open(input_path) as f:
        conceptnet_json_list = json.load(f)
    correct_all_type=0
    total_all_type=0

    for efficiency_type in ["runtime","memory"]:
        accuracy,correct,total=check_accuracy(conceptnet_json_list,efficiency_type)
        print(f"{efficiency_type} accuracy: {accuracy} correct: {correct} total: {total}")
        correct_all_type+=correct
        total_all_type+=total
        #save accuracy in file
        with open(f'accuracy_genimi_v2.txt', 'a') as f:
            f.write(f"{efficiency_type} accuracy: {accuracy} correct: {correct} total: {total}")
    accuracy=correct_all_type/total_all_type
    correct=correct_all_type
    total=total_all_type
    #save accuracy in file
    with open(f'accuracy_genimi_v2.txt', 'a') as f:
        f.write(f'{accuracy} {correct} {total}')
    
    print("all",accuracy,correct_all_type,total_all_type)
 
    
    
input_path="judgement_samples_200_gemini-2.0-flash.json"
compute(input_path)