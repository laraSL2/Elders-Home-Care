from flask import Blueprint, request, jsonify
from app.services import split_care_plan
import io

care_plan_spilt_bp = Blueprint('care_plan_split', __name__)

@care_plan_spilt_bp.route('/split_care_plan', methods=['POST'])
def split_care_plan_route():
    if 'care_plan_file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['care_plan_file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if file:
        # Read the contents of the file
        file_contents = file.read().decode('utf-8')
        
        # Process the file contents
        split_plan = split_care_plan(file_contents)
        
        # Return the processed data
        return jsonify(split_plan)
    
    return jsonify({"error": "Error processing file"}), 500