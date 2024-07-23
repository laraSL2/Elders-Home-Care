from flask import current_app
import json
from app.utils.care_note_prompts import CARE_NOTE_TEMPLATE
from typing import Tuple, Optional


def enhance_note(original_care_note: str) -> Tuple[Optional[str], Optional[str]]:
    try:
        gemini = current_app.gemini
        prompt = CARE_NOTE_TEMPLATE.format(input_text=original_care_note)
        
        response = gemini.run_text_model(prompt, model_name="gemini-1.5-flash", temperature=0.2)
        
        response = response.replace("```", "").replace("json\n{", "{")
        response_json = json.loads(response)
        
        enhanced_text = response_json.get("enhanced_text", "")
        suggestions_text = response_json.get("suggestions_text", "")
        
        return enhanced_text, suggestions_text
    except json.JSONDecodeError:
        current_app.logger.error("Failed to parse JSON response from Gemini")
        return None, None
    except KeyError as e:
        current_app.logger.error(f"Missing key in JSON response: {str(e)}")
        return None, None
    except Exception as e:
        current_app.logger.error(f"Unexpected error in enhance_note: {str(e)}")
        return None, None