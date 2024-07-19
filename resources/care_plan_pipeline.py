import concurrent.futures
from typing import List, Dict
import time
from care_plan_add_review import standardize_care_plan
from care_all_plan import final_care_plan
import sub_plan

def process_subplan(sub):
     res = standardize_care_plan(sub)
     # time.sleep(2)
     return res


def pipeline(subplans: List[str], combine_instructions: str) -> Dict:
     start_time = time.time()
    
    # Use ThreadPoolExecutor to process subplans concurrently
     # with concurrent.futures.ThreadPoolExecutor() as executor:
     #    standardized_subplans = list(executor.map(process_subplan, subplans))
     standardized_subplans = []
     for sub in subplans:
          res = standardize_care_plan(sub)
          standardized_subplans.append(res)


     
     # Call final_care_plan with the standardized subplans
     print("\n\nCall final_care_plan with the standardized subplans")
     parsed_response = final_care_plan(*standardized_subplans, combine_instructions=combine_instructions)
     
     end_time = time.time()
     inference_time = end_time - start_time
     print(f"Inference Time: {inference_time} seconds")
     
     return parsed_response

# Example usage
sub_plan_list = [sub_plan.sub_plan_1, sub_plan.sub_plan_2, sub_plan.sub_plan_3, 
                 sub_plan.sub_plan_4, sub_plan.sub_plan_5, sub_plan.sub_plan_6]
combine_instructions = sub_plan.combine_instructions

result = pipeline(sub_plan_list, combine_instructions)
print(result)