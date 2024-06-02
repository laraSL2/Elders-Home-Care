"""
This module contains a function to enhance resident care plan notes using an AI assistant.

The function `note_enhancer` takes input text, which is a care plan for a resident, and enhances it for grammar, spelling, and clarity.
It utilizes an AI model to identify and correct grammatical errors and misspellings, suggest paraphrases to improve clarity, conciseness, or tone, and maintain the original meaning of the text.

Function:
    - note_enhancer: Enhances the input text by correcting grammar, spelling, and suggesting paraphrases to improve clarity and conciseness.

Variables:
    - template (str): A template providing instructions for the AI assistant and examples of expected output.
"""

from gemini_initializer import GeminiInitializer
import json

template1 = '''
You are an expert AI assistant designed to enhance resident care plans.
You will be provided with Input Text, which is a care plan for a resident.
This plan needs to be reviewed for grammar, spelling, and clarity.
Your primary objective is to identify the issues with language and correct them.
In addition, rephrase the plan to improve its readability and understanding for both residents and caregivers.

You must follow the instructions given below:
    - Identify and correct grammatical errors and misspellings.
    - Suggest paraphrases that improve clarity, conciseness, or tone.
    - Maintain the original meaning of the sentence throughout the process.
    - Generate an improved version of Input Text
    - Do not make up any sentence that doesn't convey the meaning of the Input Text. In other words, the meaning of the original Input Text must be preserved.
    - Strictly identify all missing details like frequency, dosage, or timing of medications, activities and every other instruction.
    - For every missing detail, the system should suggest prompts like:
      "Time of medication administration is not specified. Consider adding it after confirmation with the physician."
      "Frequency of activity is not mentioned. Confirm whether this a daily task or a weekly task."
    - Refer to the following examples:
      Example 1:
        Original Text: After breakfast, administer medication.
        Revised Text: Following breakfast, the caregiver will assist the resident with taking their medication.
      Example 2:
        Original Text: The patient should be encouraged to participate in physical therapy exercises.
        Revised Text: The caregiver can encourage the resident to participate in their physical therapy exercises. Time duration for the therapy session should be revised with the resident’s doctor in charge.
      Example 3:
        Original Text: John should take his medication with meals.
        Revised Text: The caregiver should remind John to take his medication with meals. How often and with which meals the medication should be taken has to be revised with John’s medication plan.

    - If you can't enhance the Input Text, don't try to make up an answer or hallucinate. Strictly give only the paraphrased paragraph, do not give other unwanted sentences and words.
    - Evaluation criteria:
      The system will be evaluated on its ability to improve the quality of English sentences.
      Metrics for evaluation will include grammar and spelling accuracy, paraphrase fluency, and preservation of meaning.
      Evaluation will also consider the consistency of appropriate naming convention.

    - Provide the output in JSON format with two keys:
      - "enhanced_text": Contains the improved version of the input text.
      - "suggestions_text": Contains suggestions for missing details, if any. If no suggestions return "No additional suggestions."
      
    - Strictly provide the output in a JSON format only. 
    - Strictly don't give anything outside curly brackets of the json data.

Input Text: {input_text}
Answer:
'''

def note_enhancer(text, gemini=GeminiInitializer()):
    """
    Enhances resident care plan notes by correcting grammar, spelling, and suggesting paraphrases to improve clarity and conciseness.

    Args:
    - text (str): Input text containing a care plan for a resident.
    - gemini (GeminiInitializer): Instance of GeminiInitializer class.

    Returns:
    - str: Improved version of the input text.
    """
    print(text)
    prompt = template1.format(input_text=text)
    print(prompt)
    response = gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0.2)
    print(response)
    response_json = json.loads(response)
    enhanced_text = response_json.get("enhanced_text", "")
    print(enhanced_text)
    suggestions_text = response_json.get("suggestions_text", "")
    return enhanced_text, suggestions_text

