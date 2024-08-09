from flask import Blueprint, request, jsonify
from app.services import summarize_care_story

care_story_bp = Blueprint('care_story', __name__)

@care_story_bp.route('/care_story', methods=['POST'])
def care_story():
    data = request.json
    care_story = data.get("care_story")
    
    if not care_story:
        return jsonify({"error": "Please enter care story"}), 400

    response = summarize_care_story(care_story)
    return jsonify({"care_story_response": response})