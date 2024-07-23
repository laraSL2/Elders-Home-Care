import json
from typing import List, Dict, Optional
import re

def format_care_plan(payload):
    try:  
         data = json.loads(payload)
    except:
         data = payload
         
    care_plans = data['care_plan']
    output = ""

    for i, subplan in enumerate(care_plans, 1):
        output += f"Subplan {str(i).zfill(2)} \n {subplan['SubplanTitle']}\n\n"
        
        # Assessed Current Situations
        output += "Assessed current situations\n"
        for situation in subplan['sub_plan']['AssessedCurrentSituations']:
            if situation.strip():
                output += f"{situation.strip()}\n"
        
        # Care Needs
        output += "\nCare needs\n"
        for need in subplan['sub_plan']['CareNeeds']:
            output += f"{need.strip()}\n"
        
        # Outcomes and Goals
        output += "\nOutcome/goal\n"
        for goal in subplan['sub_plan']['OutcomesAndGoals']:
            output += f"{goal.strip()}\n"
        
        # Description of Care Actions
        output += "\nDescription of care actions\n"
        for action in subplan['sub_plan']['DescriptionOfCareActions']:
            output += f"{action.strip()}\n"
        
        # Reviews
        output += "\nReviews\n"
        for review in subplan['sub_plan']['Reviews']:
            output += f"{review.strip()}\n"
        
        output += "\n"
    
    return output.strip()


def clean_empty_sections(data: Dict) -> Dict:
    print("""Clean specific sections that were empty in the original or are empty lists.""")
    
    for subplan in data.get('FinalOutputGeneration', {}).get('Subplans', []):
        enhanced_care_plan = subplan.get('EnhancedCarePlan', {})

        # Clean AssessedCurrentSituations
        if 'AssessedCurrentSituations' in enhanced_care_plan:
            if not enhanced_care_plan['AssessedCurrentSituations'] or enhanced_care_plan['AssessedCurrentSituations'] == ["This section was empty in the original and remains empty."]:
                enhanced_care_plan['AssessedCurrentSituations'] = []
            elif isinstance(enhanced_care_plan['AssessedCurrentSituations'], str):
                enhanced_care_plan['AssessedCurrentSituations'] = [enhanced_care_plan['AssessedCurrentSituations']]

        # Clean CareNeeds
        if 'CareNeeds' in enhanced_care_plan:
            if not enhanced_care_plan['CareNeeds'] or enhanced_care_plan['CareNeeds'] == ["This section was empty in the original and remains empty."]:
                enhanced_care_plan['CareNeeds'] = []
            elif isinstance(enhanced_care_plan['CareNeeds'], str):
                enhanced_care_plan['CareNeeds'] = [enhanced_care_plan['CareNeeds']]

        # Clean DescriptionOfCareActions
        if 'DescriptionOfCareActions' in enhanced_care_plan:
            if not enhanced_care_plan['DescriptionOfCareActions'] or enhanced_care_plan['DescriptionOfCareActions'] == ["This section was empty in the original and remains empty."]:
                enhanced_care_plan['DescriptionOfCareActions'] = []
            elif isinstance(enhanced_care_plan['DescriptionOfCareActions'], str):
                enhanced_care_plan['DescriptionOfCareActions'] = [enhanced_care_plan['DescriptionOfCareActions']]

        # Clean OutcomesAndGoals
        if 'OutcomesAndGoals' in enhanced_care_plan:
            if not enhanced_care_plan['OutcomesAndGoals'] or enhanced_care_plan['OutcomesAndGoals'] == ["This section was empty in the original and remains empty."]:
                enhanced_care_plan['OutcomesAndGoals'] = []
            elif isinstance(enhanced_care_plan['OutcomesAndGoals'], str):
                enhanced_care_plan['OutcomesAndGoals'] = [enhanced_care_plan['OutcomesAndGoals']]

    return data


def extract_json(text: str) -> Optional[Dict]:
    """Attempt to extract and parse JSON from the given text."""
    try:
        # First, try to parse the entire text as JSON
        return json.loads(text)
    except json.JSONDecodeError:
        # If that fails, try to find a JSON object within the text
        json_match = re.search(r'(\{.*\})', text, re.DOTALL)
        if json_match:
            try:
                # Validate that the extracted text is valid JSON
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                return None
    return None

def clean_refined_empty_sections(data: Dict) -> Dict:
    print("Clean specific sections that were empty in the original or are empty lists.")
    
    if 'RefinedCarePlan' in data:
        refined_care_plan = data['RefinedCarePlan']

        sections_to_clean = [
            'AssessedCurrentSituations',
            'CareNeeds',
            'DescriptionOfCareActions',
            'OutcomesAndGoals'
        ]

        for section in sections_to_clean:
            if section in refined_care_plan:
                if not refined_care_plan[section] or refined_care_plan[section] == ["This section was empty in the original and remains empty."]:
                    refined_care_plan[section] = []
                elif isinstance(refined_care_plan[section], str):
                    refined_care_plan[section] = [refined_care_plan[section]]

    return data



