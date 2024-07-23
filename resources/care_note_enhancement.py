"""
This module contains a function to enhance resident care note notes using an AI assistant.

The function `note_enhancer` takes input text, which is a care note for a resident, and enhances it for grammar, spelling, and clarity.
It utilizes an AI model to identify and correct grammatical errors and misspellings, suggest paraphrases to improve clarity, conciseness, or tone, and maintain the original meaning of the text.

Function:
    - note_enhancer: Enhances the input text by correcting grammar, spelling, and suggesting paraphrases to improve clarity and conciseness.

Variables:
    - template (str): A template providing instructions for the AI assistant and examples of expected output.
"""

from gemini_initializer import GeminiInitializer
import json

template1 = """
You are an expert AI assistant designed to enhance resident care notes.
You will be provided with Input Text, which is a care note for a resident.
This note needs to be reviewed for grammar, spelling, and clarity.
Your primary objective is to identify the issues with language and correct them.
In addition, rephrase the note to improve its readability and understanding for both residents and caregivers.

You must follow the instructions given below:
    - Identify and correct grammatical errors and misspellings.
    - Your answer must be in standard English and use medical terms accurately and appropriately.
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
        Revised Text: The caregiver can encourage the resident to participate in their physical therapy exercises. Time duration for the therapy session should be revised with the resident's doctor in charge.
      Example 3:
        Original Text: John should take his medication with meals.
        Revised Text: The caregiver should remind John to take his medication with meals. How often and with which meals the medication should be taken has to be revised with John's medication note.

    - If you can't enhance the Input Text, don't try to make up an answer or hallucinate. Strictly give only the paraphrased paragraph, do not give other unwanted sentences and words.
    - Evaluation criteria:
      The system will be evaluated on its ability to improve the quality of English sentences.
      Metrics for evaluation will include grammar and spelling accuracy, paraphrase fluency, and preservation of meaning.
      Evaluation will also consider the consistency of appropriate naming convention.

    - You must provide the output in JSON format with two keys:
      - "enhanced_text": Contains the improved version of the input text. Must not include any suggestions here
      - "suggestions_text": Contains suggestions for missing details according to your understanding to improve the care note, if any. If no suggestions return "No additional suggestions."
      
    - Strictly provide the output in a JSON format only. 
    - Strictly don't give anything outside curly brackets of the json data.

Input Text: {input_text}
Answer:
"""

template2 = """
  You are an expert AI assistant specializing in enhancing and refining resident care notes. Your primary task is to analyze, improve, and reformat care notes to ensure clarity, accuracy, and completeness.

  You must follow the instructions given below:
  <INSTRUCTIONS>
    1. Comprehend the care note:
       - Identify key information about the resident's condition and care provided.
       - Note actions taken by caregivers and the resident's responses.
       - Assess the context to ensure all actions and observations are logically connected.
       Example:
        Input: "refused breakfast"
        Output: "The resident declined their breakfast meal when offered this morning."


    2. Fix grammar and spelling mistakes:
       - Correct grammatical errors while maintaining the original meaning.
       - Fix spelling mistakes and typos.
       Example:
        Input: "pt agitated, gave meds"
        Output: "The patient displayed signs of agitation. Prescribed medication was administered to address this state."


    3. Enhance content accuracy and completeness:
       - Ensure logical consistency and chronological order of events.
       - Infer and include implied information based on context.
       - Remove redundancies while preserving all relevant details.
       Example:
         Input: "fell outta bed last nite"
         Output: "During the night, the resident experienced a fall from their bed. Staff immediately assessed for injuries and implemented necessary safety protocols."

    4. Reformat and expand the note:
       - Organize information in a clear, chronological order.
       - Include relevant details about the care session, resident's state, and caregiver actions.
       - Enhance the note to provide a comprehensive view of the care provided.

    5. Output a concise, detailed paragraph:
       - Combine all improved information into a single, well-structured paragraph.
       - Ensure the paragraph flows logically and provides a complete picture of the care session.

    6. Identify missing details:
       - Highlight any missing information such as specific care actions, or resident responses.
       - For each missing detail, suggest a prompt for clarification.
       
    7. Identify and suggest missing critical information:
       - Highlight any absent details crucial for comprehensive care documentation.
       - Formulate specific questions to prompt for missing information.

    8. Final check:
       - Verify that the output maintains medical accuracy and professionalism.
       - Ensure all essential information from the original note is preserved and enhanced.
  </INSTRUCTIONS>
  
  Evaluation criteria:
    - Transformation of fragmented notes into complete, professional sentences
    - Accuracy and appropriateness of medical terminology
    - Logical organization and flow of information
    - Identification of critical missing details
    - Overall improvement in clarity and informativeness of the care note


  Output format:
  Provide the output in JSON format with two keys:
  - "enhanced_text": Contains the improved version of the input text. Do not include any suggestions here.
  - "suggestions_text": Contains suggestions for missing details to improve the care note. If no suggestions, return "No additional suggestions."
  
  Examples:
  
  1. Input: "John refusd breakfast. gave meds. complaned of pain in leg. helped to toilet."
     Output: 
       "enhanced_text": "John refused breakfast this morning. His prescribed medications were administered as scheduled. John complained of pain in his leg, which was noted for follow-up. He was assisted to the toilet, providing necessary support for his mobility and comfort. Staff will continue to monitor his pain levels and appetite throughout the day.",
       "suggestions_text": "Clarify the intensity and location of leg pain. Confirm if this is a new or recurring issue."
  
  2. Input: "Mary agitated today. yelling at staff. tried calming techniqes. eventually settled. didnt eat lunch."
     Output:
       "enhanced_text": "Mary displayed signs of agitation today, expressing her distress by yelling at staff members. Caregivers implemented various calming techniques to address her agitation. These efforts were eventually successful, and Mary settled down. However, she declined to eat lunch. Staff will continue to monitor her mood, employ soothing strategies as needed, and encourage nutrition at the next meal time.",
       "suggestions_text": "List the specific calming techniques used. Clarify if any alternative food or drink was offered when she refused lunch."
  
  3. Input: "Tom fell outta bed last nite. checked for injurys. seemed ok but confused. family notified."
     Output:
       "enhanced_text": "During the night, Tom experienced a fall from his bed. Staff immediately assessed him for injuries, finding no apparent physical harm. However, Tom appeared confused following the incident, which may require further medical evaluation. His family was promptly notified of the fall. Staff will continue to monitor Tom closely for any delayed symptoms or changes in his cognitive state, and implement fall prevention strategies to ensure his safety.",
       "suggestions_text": "Detail the injury assessment process. Clarify the level and duration of confusion. Confirm if medical evaluation is scheduled. Describe the fall prevention strategies to be implemented."
     
  
  Strictly provide the output in JSON format only. Do not include anything outside the JSON object.
  
  Input Text: {input_text}
  Answer:
"""

def note_enhancer(text, gemini=GeminiInitializer()):
    """
    Enhances resident care note notes by correcting grammar, spelling, and suggesting paraphrases to improve clarity and conciseness.

    Args:
    - text (str): Input text containing a care note for a resident.
    - gemini (GeminiInitializer): Instance of GeminiInitializer class.

    Returns:
    - str: Improved version of the input text.
    """
    print(text)
    prompt = template2.format(input_text=text)
    print(prompt)
    print("-----------------"*5)
    response = gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0.2)
    print(response)

    response = response.replace("```","").replace("json\n{","{")
    print(response)
    response_json = json.loads(response)
    enhanced_text = response_json.get("enhanced_text", "")
    print(enhanced_text)
    suggestions_text = response_json.get("suggestions_text", "")
    return enhanced_text, suggestions_text

