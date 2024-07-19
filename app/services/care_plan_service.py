import json
from typing import List, Dict, Optional
from datetime import date
import time
import re
from app.utils.file_handler import read_file_contents, get_upload_folder
from app.utils.care_plan_utils import format_care_plan
from app.utils.care_plan_prompts import CARE_PLAN_TEMPLATE, FB_REFINING_TEMPLATE
from flask import current_app

def extract_json(text: str) -> Optional[str]:
    """Attempt to extract JSON from the given text."""
    json_match = re.search(r'(\{.*\})', text, re.DOTALL)
    return json_match.group(1) if json_match else None

def generate_care_plan(payload: Dict) -> Optional[Dict]:
    try:
        gemini = current_app.gemini
        today = date.today()
        formatted_date = today.strftime("%d/%m/%y")
        
        elder_details = payload.get('elder_details', "")
        
        formatted_subplans = format_care_plan(payload)
        combine_instructions_file_path = get_upload_folder()
        combine_instructions = read_file_contents(combine_instructions_file_path)
        
        prompt = CARE_PLAN_TEMPLATE.format(subplans=formatted_subplans, combine_instructions=combine_instructions, current_date=formatted_date)
        print(prompt)
        response = gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
        
        json_str = extract_json(response)
        if json_str is None:
            raise ValueError("No JSON found in the response")
        
        parsed_json = json.loads(json_str)
        parsed_json["elder_details"] = elder_details
        return parsed_json
    except Exception as e:
        current_app.logger.error(f"Error in generate_care_plan: {str(e)}")
        return None

def process_care_plans(subplans: List[str], combine_instructions: str, max_retries: int = 2) -> Optional[Dict]:
    for attempt in range(max_retries):
        try:
            result = generate_care_plan({"subplans": subplans, "combine_instructions": combine_instructions})
            return result
        except Exception as e:
            current_app.logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                current_app.logger.error("Max retries reached. Unable to process care plans.")
                return None
    return None

def pipeline(subplans: List[str], combine_instructions: str) -> Optional[Dict]:
    start_time = time.time()
    
    result = process_care_plans(subplans, combine_instructions)
    
    end_time = time.time()
    inference_time = end_time - start_time
    current_app.logger.info(f"Inference Time: {inference_time} seconds")
    
    if result is None:
        current_app.logger.error("Failed to process care plans.")
    
    return result

def refine_care_plan(expert_feedback: str, user_input_information: Dict) -> Dict:
    try:
        gemini = current_app.gemini

        refining_prompt = FB_REFINING_TEMPLATE.format(
            input_data=json.dumps(user_input_information, indent=2),
            expert_feedback=expert_feedback
        )
        print(refining_prompt)
        refined_response = gemini.run_text_model(refining_prompt, model_name="gemini-1.5-pro-latest", temperature=0)

        refined_json = json.loads(refined_response)
        return refined_json
    except json.JSONDecodeError:
        current_app.logger.error("Failed to parse the refined care plan as JSON.")
        return {
            "SubplanTitle": "Error",
            "EnhancedCarePlan": {},
            "Reasoning": "Failed to parse the refined care plan as JSON."
        }
    except Exception as e:
        current_app.logger.error(f"Unexpected error in refine_care_plan: {str(e)}")
        return {
            "SubplanTitle": "Error",
            "EnhancedCarePlan": {},
            "Reasoning": f"An unexpected error occurred: {str(e)}"
        }