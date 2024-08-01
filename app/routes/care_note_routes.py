from flask import Blueprint, request, jsonify, current_app
from app.services import enhance_note, enhance_aggression_note
import sqlite3

care_note_bp = Blueprint('care_note', __name__)

@care_note_bp.route('/note_enhancement', methods=['POST'])
def note_enhancement():
    try:
        care_note = request.json.get('care_note')
        if not care_note:
            return jsonify({"error": "No care note provided"}), 400
        
        enhanced_note = enhance_note(care_note)
        
        if enhanced_note is None:
            return jsonify({"error": "Failed to enhance care note"}), 500
        
        return jsonify(enhanced_note), 200
    except Exception as e:
        current_app.logger.error(f"Unexpected error in note_enhancement: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    

@care_note_bp.route('/agg_note_enhancement', methods=['POST'])
def aggression_note_enhancement():
    try:
        data = request.json
        resident_id = data.get('resident_id')
        care_note = data.get('care_note')
        first_llm_questions_answers = data.get('first_llm_questions_answers')

        if not all([resident_id, care_note, first_llm_questions_answers]):
            return jsonify({"error": "Missing required data"}), 400

        enhanced_note = enhance_aggression_note(resident_id, care_note, first_llm_questions_answers)

        if enhanced_note is None:
            return jsonify({"error": "Failed to enhance care note"}), 500

        return jsonify(enhanced_note), 200
    except sqlite3.Error as e:
        current_app.logger.error(f"Database error in aggression_note_enhancement: {str(e)}")
        return jsonify({"error": "A database error occurred"}), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in aggression_note_enhancement: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500