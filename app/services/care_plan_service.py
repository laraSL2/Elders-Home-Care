import json
from typing import List, Dict, Optional
from datetime import date
import time
import re
from app.utils.file_handler import read_file_contents, get_upload_folder
from app.utils.care_plan_utils import format_care_plan
from app.utils.care_plan_prompts import CARE_PLAN_TEMPLATE, FB_REFINING_TEMPLATE
from flask import current_app

import json

def extract_json(text: str) -> Optional[str]:
    """Attempt to extract JSON from the given text."""
    try:
        # First, try to parse the entire text as JSON
        json.loads(text)
        return text
    except json.JSONDecodeError as e:
        print("error 1:", e)
        # If that fails, try to find a JSON object within the text
        json_match = re.search(r'(\{.*\})', text, re.DOTALL)
        if json_match:
            try:
                # Validate that the extracted text is valid JSON
                json.loads(json_match.group(1))
                return json_match.group(1)
            except json.JSONDecodeError as e:
                print("error 2:", e)
                return None
    return None


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
        print("-"*150)
        print(response)
        print("-"*150)
        json_str = extract_json(response)
        if json_str is None:
            current_app.logger.error(f"Failed to extract JSON from response: {response}")
            raise ValueError("No valid JSON found in the response")
        
        try:
            parsed_json = json.loads(json_str)
        except json.JSONDecodeError as json_error:
            current_app.logger.error(f"JSON parsing error: {str(json_error)}")
            current_app.logger.error(f"Problematic JSON string: {json_str}")
            raise json_error
        
        parsed_json["elder_details"] = elder_details
        
        return parsed_json
    except Exception as e:
        current_app.logger.error(f"Error in generate_care_plan: {str(e)}")
        return None

def process_care_plans(subplans: List[str], combine_instructions: str, max_retries: int = 2) -> Optional[Dict]:
    for attempt in range(max_retries):
        try:
            print("Attempt: ",attempt)
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