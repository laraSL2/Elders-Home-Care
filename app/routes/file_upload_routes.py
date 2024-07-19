from flask import Blueprint, request, jsonify
from app.utils.file_handler import save_uploaded_file
import os

file_upload_bp = Blueprint('file_upload', __name__)

@file_upload_bp.route('/upload_instruction', methods=['POST'])
def upload_instruction_file():
    if 'instruction_file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['instruction_file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file:
        try:
            # Save the uploaded file
            file_path = save_uploaded_file(file)
            
            if file_path:
                return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200
            else:
                return jsonify({"error": "Failed to save the file"}), 500
        except Exception as e:
            return jsonify({"error": f"Error uploading file: {str(e)}"}), 500
    
    return jsonify({"error": "Invalid file"}), 400