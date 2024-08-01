from flask import current_app
import json
from app.utils.care_note_prompts import CARE_NOTE_TEMPLATE, SECOND_LLM_CALL_TEMPLATE
from typing import Dict, Optional
from app.utils.care_plan_utils import extract_json
from app.utils.care_note_utils import format_questions_answers_dict
from app.models.resident_behavior import ResidentBehavior
from datetime import datetime
import traceback
import sqlite3

def enhance_note(original_care_note: str) -> Optional[Dict]:
    try:
        gemini = current_app.gemini
        prompt = CARE_NOTE_TEMPLATE.format(input_text=original_care_note)
        response = gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0.2)
        current_app.logger.info(f"Raw response from Gemini: {response}")  # Log the raw response

        # Use the extract_json function to parse the response
        response_json = extract_json(response)
        
        if response_json is None:
            current_app.logger.error(f"Failed to extract JSON from Gemini response: {response}")
            return None

        return response_json
    except Exception as e:
        current_app.logger.error(f"Unexpected error in enhance_note: {str(e)}")
        return None
    


def enhance_aggression_note(resident_id: str, original_care_note: str, first_llm_questions_answers: list):
    try:
        current_app.logger.info(f"Starting enhance_aggression_note for resident {resident_id}")
        current_app.logger.info(f"Original care note: {original_care_note}")
        current_app.logger.info(f"First LLM Q&A: {first_llm_questions_answers}")

        gemini = current_app.gemini
        
        # Ensure database exists and is initialized
        try:
            ResidentBehavior.create_db_if_not_exists()
        except (PermissionError, OSError) as e:
            current_app.logger.error(f"Error creating database: {str(e)}")
            # Continue processing even if database creation fails

        try:
            prev_data = ResidentBehavior.get_behavior(resident_id)
            if prev_data:
                prev_behavior_date = prev_data['current_date']
                prev_behavior_summary = prev_data['behavior_summary']
                prev_behavior_intensity = prev_data['behavior_intensity']
            else:
                prev_behavior_date = prev_behavior_summary = prev_behavior_intensity = None
        except (sqlite3.Error, PermissionError, OSError) as e:
            current_app.logger.error(f"Error when retrieving previous behavior: {str(e)}")
            prev_behavior_date = prev_behavior_summary = prev_behavior_intensity = None

        current_date = datetime.now().strftime("%Y-%m-%d")
        
        current_app.logger.info("Formatting first_llm_questions_answers")
        formatted_qa = format_questions_answers_dict(first_llm_questions_answers)

        current_app.logger.info("Preparing prompt for LLM")
        prompt = SECOND_LLM_CALL_TEMPLATE.format(
            original_care_note=original_care_note,
            first_llm_questions_answers=formatted_qa,
            previous_behavior_date=prev_behavior_date,
            previous_behavior_summary=prev_behavior_summary,
            previous_behavior_intensity=prev_behavior_intensity,
            current_date=current_date
        )
        
        current_app.logger.info("Processing with LLM")
        response = gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0.2)
        current_app.logger.info(f"Raw LLM response: {response}")

        response_json = extract_json(response)
        current_app.logger.info(f"Extracted JSON: {response_json}")

        enhanced_text = response_json['enhanced_text']
        suggestions_text = response_json['suggestions_text']
        behavior_summary = response_json['summary']['behavior_summary']
        behavior_intensity = response_json['summary']['behavior_intensity']

        current_app.logger.info("Updating database")
        try:
            ResidentBehavior.update_behavior(
                resident_id, current_date, original_care_note, behavior_summary, behavior_intensity
            )
        except (sqlite3.Error, PermissionError, OSError) as e:
            current_app.logger.error(f"Error when updating behavior: {str(e)}")
            # Continue processing even if database update fails

        current_app.logger.info("enhance_aggression_note completed successfully")
        return {
            "enhanced_text": enhanced_text,
            "suggestions_text": suggestions_text,
            "behavior_summary": behavior_summary,
            "behavior_intensity": behavior_intensity
        }
    except Exception as e:
        current_app.logger.error(f"Error in enhance_aggression_note: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return None