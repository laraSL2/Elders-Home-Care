import os
from werkzeug.utils import secure_filename
from flask import current_app

def get_upload_folder():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

def save_uploaded_file(file):
    if file and file.filename:
        filename = "combine_instructions.txt"
        upload_folder = get_upload_folder()
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    return None

def read_file_contents(file_path):
    try:
        filename = "combine_instructions.txt"
        file_path = f"{file_path}/{filename}"
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except IOError as e:
        current_app.logger.error(f"Error reading file {file_path}: {str(e)}")
        return None
    except UnicodeDecodeError:
        # If UTF-8 decoding fails, try with ISO-8859-1 encoding
        try:
            with open(file_path, 'r', encoding='iso-8859-1') as file:
                content = file.read()
            return content
        except Exception as e:
            current_app.logger.error(f"Error reading file {file_path} with ISO-8859-1 encoding: {str(e)}")
            return None

def get_file_info(file_path):
    try:
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        return {
            "file_name": file_name,
            "file_size": file_size,
            "file_path": file_path
        }
    except OSError as e:
        current_app.logger.error(f"Error getting file info for {file_path}: {str(e)}")
        return None