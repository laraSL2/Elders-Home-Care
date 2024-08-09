from flask import Blueprint, request, jsonify
from app.utils.file_handler import save_uploaded_file
import os
from app.services.care_plan_instructions_service import write_instruction, read_instructions

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


@file_upload_bp.route('/update_instruction', methods=['POST'])
def update_care_plan_instruction():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    instruction = data.get('instruction')
    if not instruction or instruction.strip() == "":
        default_instruction = "Don't combine any subplan. maintain everything as separate subplans."
        write_instruction(default_instruction)
        return jsonify({
            "error": "No valid instruction provided",
            "message": f"System is running with default instruction: '{default_instruction}'"
        }), 400

    try:
        result = write_instruction(instruction)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result), 200
    except Exception as ex:
        return jsonify({"error": f"Error updating instruction: {str(ex)}"}), 500

@file_upload_bp.route('/read_instruction', methods=['GET'])
def read_care_plan_instruction():
    try:
        result = read_instructions()
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as ex:
        return jsonify({"error": f"Error reading instruction: {str(ex)}"}), 500
