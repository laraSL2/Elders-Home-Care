from flask import Blueprint, request, jsonify
from app.services import enhance_note

care_note_bp = Blueprint('care_note', __name__)

@care_note_bp.route('/note_enhancement', methods=['POST'])
def note_enhancement():
    data = request.json
    original_care_note = data.get('care_note')
    
    if not original_care_note:
        return jsonify({"error": "Care note is required"}), 400

    enhanced_note, suggestions_note = enhance_note(original_care_note)
    return jsonify({"enhanced_note": enhanced_note, "suggestions_note": suggestions_note})