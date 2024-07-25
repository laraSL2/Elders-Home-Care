from flask import Blueprint, request, jsonify
from app.services import add_elder_data
from werkzeug.exceptions import BadRequest, InternalServerError

add_elder_bp = Blueprint('add_elder_details', __name__)

@add_elder_bp.route('/add_elder', methods=['POST'])
def add_elder():
    try:
        resident_id = request.form.get('resident_id')
        resident_name = request.form.get('resident_name')

        if not resident_id or not resident_name:
            raise BadRequest("Both resident_id and resident_name are required")

        if 'elder_details_file' not in request.files:
            raise BadRequest("No file part in the request")

        file = request.files['elder_details_file']

        if file.filename == '':
            raise BadRequest("No file selected")

        if file:
            # Read the contents of the file
            file_contents = file.read().decode('utf-8')
            
            # Process the file contents along with resident_id and resident_name
            status = add_elder_data(resident_id, resident_name, file_contents)
            
            # Return the processed data
            return jsonify(status), 200
        else:
            raise BadRequest("Error processing file")

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        # Log the error here (e.g., print(f"Error: {str(e)}") or use a proper logging system)
        return jsonify({"error": "An unexpected error occurred"}), 500