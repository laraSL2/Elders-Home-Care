from gemini_initializer import GeminiInitializer
from datetime import date

CARE_PLAN_TEMPLATE3 = """
You are an AI assistant designed to update and improve elder care plans by incorporating the most recent relevant review information. Please provide an improved version of the care plan by following these steps:

<INSTRUCTIONS>

1. Do not move existing content between sections under any circumstances.
2. Review Integration:
   a. Carefully read through the "Reviews" section
   b. Identify the most recent review by following these steps:
      - Convert all dates to a standardized format (YYYY-MM-DD) for accurate comparison
      - Compare the converted dates to find the most recent one
      - If multiple reviews share the most recent date, select the one with the most relevant information about changes in the patient's condition, medication, or care needs
      
   c. Select this review for integration into the main care plan
   d. Rewrite the selected review as a grammatically correct, clear, and concise sentence or sentences (avoid reviewer info)
      Example:
         - Original Review:
             "On 01/07/2024, the patient has shown significant improvement in their mobility. They can now walk unaided for short distances, which they couldn't do before. However, there has been a slight increase in joint pain, particularly in the mornings. Adjustments to the physical therapy routine may be necessary to address this."
         - Rewritten Review:
             "The patient has shown significant improvement in mobility, now able to walk unaided for short distances. However, there is a slight increase in joint pain, particularly in the mornings, suggesting the need for adjustments to the physical therapy routine."
   e. Ensure the converted review maintains all relevant information from the original entry
   f. Determine which of the following sections it best fits into:
      - Care needs
      - Outcome/goal
      - Description of care actions
   g. Insert the converted review into the appropriate section
   h. Ensure the new information flows logically with the existing content in that section
   i. Clearly mark any new additions with [NEW] tags

3. Standardize the existing plan for grammatical correctness, clarity, and completeness:
   - Ensure all text is clear, professionally presented, and free of grammatical errors.

4. After updating each section, verify that all original content remains in its original place.

</INSTRUCTIONS>

General Guidelines:
- Work only within the sections listed above
- Do not create new sections or subsections
- Maintain the original structure of each section
- Use clear, concise language throughout
- Ensure all critical information is included while eliminating redundancies
- Use consistent terminology and formatting throughout the document

IMPORTANT: New information should only be added to the appropriate section, never used to replace or relocate existing content. Failure to follow these instructions could result in critical care information being misplaced or lost.

Please ensure that existing content remains in its original sections without being moved or relocated. You must strictly adhere to this instruction.

OUTPUT_FORMAT
[SECTION_NAME]

Assessed current situations:

Care needs:
[Updated content]

Outcome/goal:
[Updated content]

Description of care actions:
[Updated content]

Reviews:

INPUT:
{plan_subsection}

The Elder Profile is provided as additional context. Only use information from the Elder Profile when it's specifically relevant to updating a section of the care plan or when explicitly instructed to do so. Do not automatically incorporate all elder profile information into the care plan.
Elder Profile:
{profile}
OUTPUT
"""



CARE_PLAN_TEMPLATE = """
You are an AI assistant designed to update and improve elder care plans by incorporating the most recent relevant review information. Please provide an improved version of the care plan by following these steps:

<INSTRUCTIONS>

1. Do not move existing content between sections under any circumstances.
2. Review Integration:
   a. Carefully read through the "Reviews" section
   b. Identify the most recent review by following these steps:
      - Convert all dates to a standardized format (YYYY-MM-DD) for accurate comparison
      - Compare the converted dates to find the most recent one
      - If multiple reviews share the most recent date, select the one with the most relevant information about changes in the patient's condition, medication, or care needs
      
   c. Select this review for integration into the main care plan
   d. Rewrite the selected review as a grammatically correct, clear, and concise sentence or sentences (avoid reviewer info)
      Example:
         - Original Review:
             "On 01/07/2024, the patient has shown significant improvement in their mobility. They can now walk unaided for short distances, which they couldn't do before. However, there has been a slight increase in joint pain, particularly in the mornings. Adjustments to the physical therapy routine may be necessary to address this."
         - Rewritten Review:
             "The patient has shown significant improvement in mobility, now able to walk unaided for short distances. However, there is a slight increase in joint pain, particularly in the mornings, suggesting the need for adjustments to the physical therapy routine."
   e. Ensure the converted review maintains all relevant information from the original entry
   f. Determine which of the following sections it best fits into:
      - Care needs
      - Outcome/goal
      - Description of care actions
   g. Insert the converted review into the appropriate section
   h. Ensure the new information flows logically with the existing content in that section
   

3. Standardize the existing plan for grammatical correctness, clarity, and completeness:
   - Ensure all text is clear, professionally presented, and free of grammatical errors.

4. After updating each section, verify that all original content remains in its original place.

</INSTRUCTIONS>

General Guidelines:
- Work only within the sections listed above
- Do not create new sections or subsections
- Maintain the original structure of each section
- Use clear, concise language throughout
- Ensure all critical information is included while eliminating redundancies
- Use consistent terminology and formatting throughout the document

IMPORTANT: New information should only be added to the appropriate section, never used to replace or relocate existing content. Failure to follow these instructions could result in critical care information being misplaced or lost.

Please ensure that existing content remains in its original sections without being moved or relocated. You must strictly adhere to this instruction.

OUTPUT_FORMAT
[SECTION_NAME]

Assessed current situations:

Care needs:
[Updated content]

Outcome/goal:
[Updated content]

Description of care actions:
[Updated content]

Reviews:

INPUT:
{plan_subsection}
OUTPUT
"""

# i. Clearly mark any new additions with [NEW] tags

# Note: Do not include a "Reviews" section in the output. The review information should be integrated into the appropriate sections above.

CARE_PLAN_TEMPLATE2 = """
You are an AI assistant designed to update and improve elder care plans by incorporating the most recent relevant review information. Please provide an improved version of the care plan by following these steps:

<INSTRUCTIONS>

1. Do not move existing content between sections under any circumstances.
2. Review Integration:
   a. Carefully read through the "Reviews" section
   b. Identify the most recent review by following these steps:
      - Convert all dates to a standardized format (YYYY-MM-DD) for accurate comparison
      - Compare the converted dates to find the most recent one
      - If multiple reviews share the most recent date, select the one with the most relevant information about changes in the patient's condition, medication, or care needs
      
   c. Select this review for integration into the main care plan
   d. Rewrite the selected review as a grammatically correct, clear, and concise sentence or sentences (avoid reviewer info)
      Example:
         - Original Review:
             "On 01/07/2024, the patient has shown significant improvement in their mobility. They can now walk unaided for short distances, which they couldn't do before. However, there has been a slight increase in joint pain, particularly in the mornings. Adjustments to the physical therapy routine may be necessary to address this."
         - Rewritten Review:
             "The patient has shown significant improvement in mobility, now able to walk unaided for short distances. However, there is a slight increase in joint pain, particularly in the mornings, suggesting the need for adjustments to the physical therapy routine."
   e. Ensure the converted review maintains all relevant information from the original entry
   f. Determine which of the following sections it best fits into:
      - Care needs
      - Outcome/goal
      - Description of care actions
   g. Insert the converted review into the appropriate section
   h. Ensure the new information flows logically with the existing content in that section
   

3. Standardize the existing plan for grammatical correctness, clarity, and completeness:
   - Ensure all text is clear, professionally presented, and free of grammatical errors.

4. After updating each section, verify that all original content remains in its original place.

5. Give the output in markup language.

6. Format the output using markup language:
   - Use HTML tags to structure the document
   - Enclose section names in <h2> tags
   - Use <p> tags for paragraphs
   - Use <ul> and <li> tags for unordered lists
   - Use <strong> tags for emphasis where appropriate
   - Use <br> tags for line breaks within paragraphs if needed
   
</INSTRUCTIONS>

General Guidelines:
- Work only within the sections listed above
- Do not create new sections or subsections
- Maintain the original structure of each section
- Use clear, concise language throughout
- Ensure all critical information is included while eliminating redundancies
- Use consistent terminology and formatting throughout the document

IMPORTANT: New information should only be added to the appropriate section, never used to replace or relocate existing content. Failure to follow these instructions could result in critical care information being misplaced or lost.

Please ensure that existing content remains in its original sections without being moved or relocated. You must strictly adhere to this instruction.

OUTPUT_FORMAT
<h1>[SECTION_NAME]</h1>

<h2>Assessed current situations:</h2>

<h2>Care needs:</h2>
[Updated content]

<h2>Outcome/goal:</h2>
[Updated content]

<h2>Description of care actions:</h2>
[Updated content]

<h2>Reviews:</h2>
[Existing reviews remain unchanged]
INPUT:
{plan_subsection}
OUTPUT
"""

global standardize_care_plan_llm
standardize_care_plan_llm=GeminiInitializer()

TEMP = """
You are an expert AI assistant specializing in enhancing and refining resident care plan. Your primary task is to analyze, improve, and reformat care notes to ensure clarity, accuracy, and completeness.
<INSTRUCTIONS>

1. Correct all grammatical errors.
2. Enhance overall quality:
   - Improve clarity and coherence
   - Refine style and word choice
   - Ensure appropriate tone and formality
3. Ensure completeness:
   - Add any missing crucial information
   - Elaborate on underdeveloped ideas
   - Remove unnecessary repetition
5. Verify accuracy:
   - Cross-check facts and figures.
   - Correct any factual inaccuracies.
   - Ensure that all medical terminologies are used correctly.
</INSTRUCTIONS>

Please ensure that existing content remains in its original sections without being moved or relocated. You must strictly adhere to this instruction.

INPUT:
{plan_subsection}
OUTPUT
"""
TEMP2 = """
You are an expert AI assistant specializing in enhancing and refining resident care plans. Your primary task is to analyze, improve, and reformat care notes to ensure clarity, accuracy, and completeness.

<INSTRUCTIONS>

1. Correct all grammatical errors.
2. Enhance overall quality:
   - Improve clarity and coherence.
   - Refine style and word choice.
   - Ensure appropriate tone and formality.
3. Ensure completeness:
   - Add any missing crucial information.
   - Elaborate on underdeveloped ideas.
   - Remove unnecessary repetition.
4. Standardize formatting:
   - Use consistent headings and subheadings.
   - Apply uniform bullet points and numbering.
   - Ensure consistent use of fonts and styles.
5. Verify accuracy:
   - Cross-check facts and figures.
   - Correct any factual inaccuracies.
   - Ensure that all medical terminologies are used correctly.
6. Improve readability:
   - Break down long sentences into shorter, more digestible ones.
   - Use paragraphs to separate different ideas.
   - Highlight key points for quick reference.
7. Maintain confidentiality:
   - Ensure no personal or sensitive information is exposed.
   - Anonymize any resident-specific details.

</INSTRUCTIONS>

Please ensure that existing content remains in its original sections without being moved or relocated. You must strictly adhere to this instruction.

INPUT:
{plan_subsection}
OUTPUT:
"""
def standardize_text(text):
     prompt = TEMP.format(plan_subsection=text)
     print("????????????????????????????????"*5)
     response = standardize_care_plan_llm.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
     print(response)
     return response

def standardize_care_plan(text):
    """
    Enhances resident care note notes by correcting grammar, spelling, and suggesting paraphrases to improve clarity and conciseness.

    Args:
    - text (str): Input text containing a care plan subsection for a resident.
    - gemini (GeminiInitializer): Instance of GeminiInitializer class.

    Returns:
    - str: Updated version of the Care Plan.
    
    """
    today = date.today()

    # Format: DD/MM/YYYY
    formatted_date = today.strftime("%d/%m/%y")

    
    print("Today's date:", formatted_date)
    prompt = CARE_PLAN_TEMPLATE.format(plan_subsection=text)
    print("-----------------"*5)
    response = standardize_care_plan_llm.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
    print(response)
    
    response = standardize_text(response)

#     response = response.replace("```","").replace("json\n{","{")
#     print(response)
#     response_json = json.loads(response)
#     enhanced_text = response_json.get("enhanced_text", "")
#     print(enhanced_text)
#     suggestions_text = response_json.get("suggestions_text", "")
    return response


