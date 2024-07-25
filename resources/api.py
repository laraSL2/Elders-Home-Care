from flask import Flask, request, jsonify
# from dotenv import load_dotenv
# from datetime import datetime
# from io import BytesIO
import json
import base64
import os
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter
import textwrap as tw
from fb_refining_care_plan import care_plane_flow, generate_refined_care_plan
from care_note_enhancement import note_enhancer
# from care_plan_generator import generate_plan
# from knowledge_graph import add_patient, get_next_patient_id
from gemini_initializer import GeminiInitializer
# from graph_initializer import GraphInitializer
# from retrive_ids import getID, get_elder_details
# from sqlite_db import ElderDB, CarePlanDB, CareNoteDB
# from rag_expert.generate_expert_suggestions import get_llm_and_retriever
from flask_cors import CORS 
# from care_plan_add_review import standardize_care_plan
# load_dotenv()
from care_plan import pipeline

app = Flask(__name__)
CORS(app)

# Initializing objects
my_gemini = GeminiInitializer()
# my_graph = GraphInitializer()
# ids_container = getID()
# elderDB = ElderDB("database/elder_db.db")
# carePlanDB = CarePlanDB("database/care_plane_db.db")
# careNoteDB = CareNoteDB("database/care_note_db.db")
# mv_retriever, expert_llm = get_llm_and_retriever()

# def create_pdf(content):
#     buffer = BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
#                             topMargin=72, bottomMargin=18)
#     Story = []
#     styles = getSampleStyleSheet()
#     sections = content.split("**")
#     for index, section in enumerate(sections):
#         if section.strip():
#             if index == 0: 
#                 ptext = '<font size=20 color="red"><b>%s</b></font>' % section.strip()
#                 ptext = ptext.replace("#","")
#                 Story.append(Paragraph(ptext, styles["Heading1"]))
#             elif section[-1] == ":":
#                 ptext = '<font size=14 color="blue"><b>%s</b></font>' % section.strip()
#                 Story.append(Paragraph(ptext, styles["Heading2"]))
#             else:
#                 ptext = '<font size=12>%s</font>' % section.strip()
#                 Story.append(Paragraph(ptext, styles["BodyText"]))
#                 Story.append(Spacer(1, 0.2 * inch))
#     doc.build(Story)
#     buffer.seek(0)
#     return buffer

# @app.route('/add_new_elder', methods=['POST'])
# def add_new_elder():
#     data = request.json
#     print(data)
#     elder_id = data.get('elder_id')
#     file_data = data.get('file_data')
#     if not elder_id or not file_data:
#         return jsonify({"error": "Elder ID and file data are required"}), 400

#     state = add_patient(my_gemini, my_graph, elder_id, care_note_mode=False, care_note="", data=file_data)
#     if state:
#         return jsonify({"message": "Elder added successfully"}), 201
#     else:
#         return jsonify({"error": "There was an error while adding the Elder"}), 500

@app.route('/note_enhancement', methods=['POST'])
def note_enhancement():
    data = request.json
    original_care_note = data.get('care_note')
    print(original_care_note)
    if not original_care_note:
        return jsonify({"error": "Care note is required"}), 400

    enhanced_note, suggestions_note = note_enhancer(original_care_note, my_gemini)
    # careNoteDB.insert_data(original_note=original_care_note, care_note=enhanced_note)
    return jsonify({"enhanced_note": enhanced_note, "suggestions_note": suggestions_note})


@app.route('/plan_generation', methods=['POST'])
def plan_generation():
    data = request.json
    care_plan = data.get('care_plan',[])
    profile = data.get('elder_profile',"")
    combine_instructions = data.get('combine_instructions',"")
    if not care_plan:
        return jsonify({"error": "Please enter the sub plan"}), 400

    care_plan = pipeline(care_plan, combine_instructions)
    return jsonify({"care_plan": care_plan})
    

@app.route('/feedback_plan_generation', methods=['POST'])
def feedback_plan_generation():
    data = request.json
    care_plan = data.get('care_plan')
    feedback = data.get('feedback')
    if not care_plan:
        return jsonify({"error": "Please enter care plan"}), 400
    if not feedback:
        return jsonify({"care_plan": care_plan})
    
    care_plan = generate_refined_care_plan(feedback,care_plan)

    return jsonify({"care_plan": care_plan})


from care_story import care_story_summarizer
@app.route('/care_story', methods=['POST'])
def care_story():
    data = request.json
    care_story = data.get("care_story")
    
    if not care_story:
        return jsonify({"error": "Please enter care story"}), 400

    response = care_story_summarizer(care_story=care_story)
    return jsonify({"care_story_response": response})





if __name__ == '__main__':
    app.run(debug=True,port=8001,host='0.0.0.0')
