import os
from flask import current_app
from app.utils.file_handler import get_upload_folder


def write_instruction(instructions):
    try:
        upload_folder = get_upload_folder()
        file_path = os.path.join(upload_folder, "combine_instructions.txt")
        with open(file_path, 'w') as file:
            file.write(instructions)
        return {"message": "Instructions written successfully","path":upload_folder}
    except Exception as e:
        return {"error": f"Error writing instructions: {str(e)}"}

def read_instructions():
    try:
        upload_folder = get_upload_folder()
        file_path = os.path.join(upload_folder, "combine_instructions.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                instructions = file.read()
            return {"existing_instructions": instructions}
        else:
            return {"error": "Instructions file not found"}
    except Exception as e:
        return {"error": f"Error reading instructions: {str(e)}"}