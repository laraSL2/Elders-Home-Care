from flask import Blueprint, request, jsonify
from app.services import generate_care_plan, refine_care_plan

care_plan_bp = Blueprint('care_plan', __name__)

@care_plan_bp.route('/plan_generation', methods=['POST'])
def plan_generation():
    data = request.json
    care_plan = data.get('care_plan', [])
    
    if not care_plan:
        return jsonify({"error": "Please enter the sub plan"}), 400
    generated_plan = generate_care_plan(data)
    
    return jsonify(generated_plan)


@care_plan_bp.route('/feedback_plan_generation', methods=['POST'])
def feedback_plan_generation():
    data = request.json
    user_input_information = data.get('sub_plan')
    feedback = data.get('instructions')
    
    if not user_input_information:
        return jsonify({"error": "Please provide subplan information"}), 400
    
    if not feedback:
        return jsonify({"error": "Please provide instructions for refinement"}), 400
    
    refined_plan = refine_care_plan(feedback, user_input_information)
    
    if "error" in refined_plan:
        return jsonify({"error": refined_plan["error"]}), 500
    
    return jsonify(refined_plan)