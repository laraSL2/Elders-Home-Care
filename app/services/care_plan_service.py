import json
from typing import List, Dict, Optional
from datetime import date
import time
import re
from app.utils.file_handler import read_file_contents, get_upload_folder
from app.utils.care_plan_utils import format_care_plan
from app.utils.care_plan_prompts import CARE_PLAN_TEMPLATE, FB_REFINING_TEMPLATE
from flask import current_app
from app.utils.care_plan_utils import clean_empty_sections, extract_json, clean_refined_empty_sections
import json



def generate_care_plan(payload: Dict) -> Optional[Dict]:
    try:
        gemini = current_app.gemini
        today = date.today()
        formatted_date = today.strftime("%d/%m/%y")
        
        elder_details = payload.get('elder_details', "")
        
        # formatted_subplans = format_care_plan(payload)
        # try:  
        #     data = json.loads(payload)
        # except:
        #     data = payload
        formatted_subplans = payload['care_plan']
        combine_instructions_file_path = get_upload_folder()
        try:
            combine_instructions = read_file_contents(combine_instructions_file_path)
            if not combine_instructions:
                combine_instructions = "Don't combine any subplan. maintain everything as separate subplans."
                current_app.logger.warning("Combine instructions file was empty. Using default instructions.")
        except Exception as ex:
            combine_instructions = "Don't combine any subplan. maintain everything as separate subplans."
            current_app.logger.warning(f"Failed to read combine instructions file: {str(ex)}. Using default instructions.")
        
        prompt = CARE_PLAN_TEMPLATE.format(subplans=formatted_subplans, combine_instructions=combine_instructions, current_date=formatted_date)
        print(prompt)
        response = gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
        print("-"*150)
        print(response)
        print("-"*150)
        
        try:
            parsed_json = extract_json(response)
            if parsed_json is None:
                current_app.logger.error(f"Failed to extract JSON from response: {response}")
                raise ValueError("No valid JSON found in the response")

            cleaned_json = clean_empty_sections(parsed_json)
        except json.JSONDecodeError as json_error:
            current_app.logger.error(f"JSON parsing error: {str(json_error)}")
            current_app.logger.error(f"Problematic JSON string: {response}")
            raise json_error
        except Exception as e:
            current_app.logger.error(f"Unexpected error: {str(e)}")
            raise e
        
        cleaned_json["elder_details"] = elder_details
        
        return cleaned_json
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
        
        refined_response = gemini.run_text_model(refining_prompt, model_name="gemini-1.5-pro-latest", temperature=0)
        print(refined_response)
        refined_json = extract_json(refined_response)
        refined_json = clean_refined_empty_sections(refined_json)
        if refined_json is None:
            current_app.logger.error(f"Failed to extract JSON from response: {refined_response}")
            raise ValueError("No valid JSON found in the response")

        return refined_json

    except json.JSONDecodeError as json_error:
        current_app.logger.error(f"JSON parsing error: {str(json_error)}")
        current_app.logger.error(f"Problematic JSON string: {refined_response}")
        return {
            "SubplanTitle": "Error",
            "EnhancedCarePlan": {},
            "Reasoning": "Failed to parse the refined care plan as JSON."
        }
    except ValueError as value_error:
        current_app.logger.error(f"Value error: {str(value_error)}")
        return {
            "SubplanTitle": "Error",
            "EnhancedCarePlan": {},
            "Reasoning": str(value_error)
        }
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return {
            "SubplanTitle": "Error",
            "EnhancedCarePlan": {},
            "Reasoning": "An unexpected error occurred."
        }
