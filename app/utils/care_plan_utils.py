import json

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


