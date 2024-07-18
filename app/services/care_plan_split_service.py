import json
from datetime import datetime
import concurrent.futures
from typing import Dict, List, Optional
from flask import current_app

def split_care_plan_sections(input_text: str) -> Dict:
    try:
        sections = {
            "AssessedCurrentSituations": [],
            "CareNeeds": [],
            "DescriptionOfCareActions": [],
            "OutcomesAndGoals": [],
            "Reviews": []
        }
        
        lines = input_text.split('\n')
        
        current_section = None
        review_section = False
        subplan_title = None
        content_buffer = []
        
        for line in lines:
            line = line.strip()
            
            if line and not subplan_title:
                subplan_title = line
            elif "Assessed current situations" in line:
                if current_section and content_buffer:
                    sections[current_section].append(' '.join(content_buffer))
                current_section = "AssessedCurrentSituations"
                content_buffer = []
            elif "Care needs" in line:
                if current_section and content_buffer:
                    sections[current_section].append(' '.join(content_buffer))
                current_section = "CareNeeds"
                content_buffer = []
            elif "Outcome/goal" in line or "Outcomes and Goals" in line:
                if current_section and content_buffer:
                    sections[current_section].append(' '.join(content_buffer))
                current_section = "OutcomesAndGoals"
                content_buffer = []
            elif "Description of care actions" in line or "DescriptionOfCareActions" in line:
                if current_section and content_buffer:
                    sections[current_section].append(' '.join(content_buffer))
                current_section = "DescriptionOfCareActions"
                content_buffer = []
            elif "Reviews" in line:
                if current_section and content_buffer:
                    sections[current_section].append(' '.join(content_buffer))
                current_section = "Reviews"
                review_section = True
                content_buffer = []
            elif review_section and is_new_review(line):
                if content_buffer:
                    sections["Reviews"].append(' '.join(content_buffer))
                content_buffer = [line]
            elif current_section:
                content_buffer.append(line)
        
        if current_section and content_buffer:
            sections[current_section].append(' '.join(content_buffer))
        
        care_plan = {
            "SubplanTitle": subplan_title,
            "sub_plan": sections
        }
        
        return care_plan
    except Exception as e:
        current_app.logger.error(f"Error in split_care_plan_sections: {str(e)}")
        return {"error": f"Failed to split care plan sections: {str(e)}"}

def is_new_review(line: str) -> bool:
    parts = line.split()
    return len(parts) > 2 and parts[0].count('/') == 2

def process_subplan(subplan: str) -> Dict:
    try:
        return split_care_plan_sections(subplan)
    except Exception as e:
        current_app.logger.error(f"Error processing subplan: {str(e)}")
        return {"error": f"Failed to process subplan: {str(e)}"}

def split_care_plan(input_text: str, max_workers: int = 5) -> Dict:
    try:
        input_text = input_text.replace("\n\n", " ")
        subplan_list = input_text.split("<br>")
        formatted_subplans = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_subplan = {executor.submit(process_subplan, subplan.strip()): subplan for subplan in subplan_list}
            for future in concurrent.futures.as_completed(future_to_subplan):
                result = future.result()
                if "error" not in result:
                    formatted_subplans.append(result)
                else:
                    current_app.logger.warning(f"Skipping subplan due to error: {result['error']}")
        
        return {"split_plans": formatted_subplans}
    except Exception as e:
        current_app.logger.error(f"Error in split_care_plan: {str(e)}")
        return {"error": f"Failed to split care plan: {str(e)}"}