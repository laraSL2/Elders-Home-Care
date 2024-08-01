import requests
import json
import random
from datetime import datetime, timedelta

API_URL = "http://localhost:8001/api/care_note/aggression_note_enhancement"
API_URL = "http://127.0.0.1:8001/agg_note_enhancement"

def generate_care_note():
    behaviors = ["agitated", "calm", "confused", "cooperative", "aggressive"]
    actions = ["during morning care", "at mealtime", "during medication administration", "in the common area", "while resting"]
    responses = ["staff provided reassurance", "required redirection", "responded well to care", "needed assistance", "refused care"]
    
    behavior = random.choice(behaviors)
    action = random.choice(actions)
    response = random.choice(responses)
    
    return f"Resident became {behavior} {action}. {response.capitalize()}."

def generate_questions_answers(care_note):
    questions = [
        "What specific behaviors did the resident display?",
        "On a scale of 1-5, how intense was the behavior?",
        "What actions did the staff take in response?",
        "Were there any triggers identified for the behavior?",
        "How did the resident respond to staff interventions?"
    ]
    
    answers = [
        f"The resident displayed {care_note.split()[2]} behavior.",
        str(random.randint(1, 5)),
        f"Staff {care_note.split('.')[-2].strip().lower()}.",
        "No clear triggers were identified.",
        "The resident's response varied."
    ]
    
    return [{"q": q, "a": a} for q, a in zip(questions, answers[:3])]

def test_api(elder_id, care_notes):
    results = []
    for care_note in care_notes:
        payload = {
            "resident_id": elder_id,
            "care_note": care_note,
            "first_llm_questions_answers": generate_questions_answers(care_note)
        }
        print(f"Sending request for elder {elder_id}:")
        print(f"URL: {API_URL}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            results.append(response.json())
            print(f"Success for elder {elder_id}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except requests.exceptions.RequestException as e:
            print(f"Error for elder {elder_id}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status code: {e.response.status_code}")
                print(f"Response content: {e.response.text}")
                try:
                    error_details = e.response.json()
                    print(f"Error details: {json.dumps(error_details, indent=2)}")
                except json.JSONDecodeError:
                    print("Could not parse error response as JSON")
        
        print("\n" + "=" * 50 + "\n")
    
    return results

def write_results_to_file(elder_id, results):
    with open(f"test/elder_{elder_id}_results.txt", "w") as f:
        f.write(f"Results for Elder {elder_id}\n")
        f.write("=" * 50 + "\n\n")
        for i, result in enumerate(results, 1):
            f.write(f"Care Note {i}:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Enhanced Text:\n{result['enhanced_text']}\n\n")
            f.write(f"Suggestions:\n{result['suggestions_text']}\n\n")
            f.write(f"Behavior Summary:\n{result['behavior_summary']}\n\n")
            f.write(f"Behavior Intensity:\n{result['behavior_intensity']}\n\n")
            f.write("=" * 50 + "\n\n")

import time
def main():
    elders = ["E001", "E002", "E003"]
    for elder in elders:
        num_notes = random.randint(5, 10)
        care_notes = [generate_care_note() for _ in range(num_notes)]
        results = test_api(elder, care_notes)
        write_results_to_file(elder, results)
        print(f"Completed testing for Elder {elder}")
        time.sleep(12)

if __name__ == "__main__":
    main()