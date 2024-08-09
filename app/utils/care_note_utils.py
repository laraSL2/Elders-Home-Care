
import json
import re
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig
from flask import current_app

# Initialize the analyzer and anonymizer
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

config = {"PERSON": OperatorConfig("replace", {"new_value": "[PII-Person]"}),
          "URL": OperatorConfig("replace", {"new_value": "[PII-URlL]"})
          }

def mask_text(text_care_note):
  # Analyze the text for PII
  analysis_results = analyzer.analyze(text_care_note,language='en')
  filtered_analysis_results = [result for result in analysis_results if (result.entity_type=="PERSON" or result.entity_type=="ADDRESS")]

  # Anonymize the detected PII using the configuration
  masked_care_note = anonymizer.anonymize(text_care_note, filtered_analysis_results,operators=config)

  return masked_care_note.text


def format_questions_answers_dict(qa_list):
    formatted_qa = []
    for qa in qa_list:
        if isinstance(qa, dict) and 'q' in qa and 'a' in qa:
            formatted_qa.append(f"Question: {qa['q']}\nAnswer: {qa['a']}")
    return "\n\n".join(formatted_qa)



def extract_json(response):
    try:
        # First, try to parse the entire response as JSON
        return json.loads(response)
    except json.JSONDecodeError:
        # If that fails, try to extract JSON from within code block
        match = re.search(r'```json\n(.*?)```', response, re.DOTALL)
        if match:
            try:
                # Replace newlines within the JSON string to handle multi-line values
                json_str = re.sub(r'(?<=:)\s*"[^"]*\n[^"]*"', lambda m: m.group().replace('\n', '\\n'), match.group(1))
                # Replace newlines between JSON elements
                json_str = re.sub(r',\s*\n\s*"', ', "', json_str)
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                current_app.logger.error(f"Failed to parse JSON within code block: {str(e)}")
        else:
            current_app.logger.error("No JSON code block found in response")
        
        current_app.logger.error(f"Raw response: {response}")
        return None