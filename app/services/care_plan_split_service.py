import json
from datetime import datetime
import concurrent.futures
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def split_care_plan_sections(input_text: str) -> Dict:
    try:
        # Split the main sections
        SubTitle, rest = input_text.split("Assessed current situations", 1)
        Assessed_current_situations, rest = rest.split("Care needs", 1)
        Care_needs, rest = rest.split("Outcome/goal", 1)
        Outcome_goal, rest = rest.split("Description of care actions", 1)
        Description_of_care_actions, Reviews = rest.split("Reviews", 1)

        # Clean up the sections
        sections = {
            "SubplanTitle": SubTitle.strip(),
            "AssessedCurrentSituations": Assessed_current_situations.strip(),
            "CareNeeds": Care_needs.strip(),
            "OutcomesAndGoals": Outcome_goal.strip(),
            "DescriptionOfCareActions": Description_of_care_actions.strip(),
            "Reviews": Reviews.strip()
        }

        # Split Reviews into separate review entries
        reviews_list = [review.strip() for review in Reviews.split('\n') if review.strip()]

        # Data validation
        for section, content in sections.items():
            if not content:
                logger.warning(f"Empty section detected: {section}")

        care_plan = {
            "SubplanTitle": sections["SubplanTitle"],
            "sub_plan": {
                "AssessedCurrentSituations": [sections["AssessedCurrentSituations"]],
                "CareNeeds": [sections["CareNeeds"]],
                "OutcomesAndGoals": [sections["OutcomesAndGoals"]],
                "DescriptionOfCareActions": [sections["DescriptionOfCareActions"]],
                "Reviews": reviews_list
            }
        }

        return care_plan
    except Exception as e:
        logger.error(f"Error in split_care_plan_sections: {str(e)}")
        return {"error": f"Failed to split care plan sections: {str(e)}"}

def process_subplan(subplan: str) -> Dict:
    try:
        return split_care_plan_sections(subplan)
    except Exception as e:
        logger.error(f"Error processing subplan: {str(e)}")
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
                    logger.warning(f"Skipping subplan due to error: {result['error']}")

        return {"split_plans": formatted_subplans}
    except Exception as e:
        logger.error(f"Error in split_care_plan: {str(e)}")
        return {"error": f"Failed to split care plan: {str(e)}"}