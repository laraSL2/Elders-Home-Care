from flask import current_app
import json
import os
from app.utils.add_elder_prompts import ADD_ELDER_TEMPLATE
from typing import Tuple, Optional
from app.utils.care_plan_utils import extract_json

def add_elder_data(resident_id, resident_name, elder_data):
    try:
        if elder_data:
            gemini = current_app.gemini
            prompt = ADD_ELDER_TEMPLATE.format(elder_details=elder_data, resident_id=resident_id, resident_name=resident_name)

            response = gemini.run_text_model(prompt, model_name="gemini-1.5-flash", temperature=0)
            print(response)
            response_json = extract_json(response)
            

            if response_json and 'Profile' in response_json and 'Resident_ID' in response_json:
                # Get the elder ID
                # Define the base directory for saving elder files
                base_dir = os.path.join(current_app.config['ELDERS_DATA_DIR'], 'Details')

                # Ensure the directory exists
                os.makedirs(base_dir, exist_ok=True)

                # Create the full file path
                file_path = os.path.join(base_dir, f"{resident_id}.json")

                # Save the JSON data to a file
                with open(file_path, 'w') as json_file:
                    json.dump(response_json, json_file, indent=4)

                return {"message": f"Elder data saved successfully for ID: {resident_id}", "file_path": file_path}, 200
            else:
                return {"error": "Invalid JSON structure returned"}, 400
        else:
            return {"error": "The file contains no information about elder"}, 400

    except json.JSONDecodeError:
        current_app.logger.error("Failed to parse JSON response from Gemini")
        return {"error": "Failed to parse JSON response"}, 500
    except KeyError as e:
        current_app.logger.error(f"Missing key in JSON response: {str(e)}")
        return {"error": f"Missing key in JSON response: {str(e)}"}, 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in add_elder_data: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}, 500