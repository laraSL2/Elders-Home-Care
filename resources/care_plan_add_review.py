from gemini_initializer import GeminiInitializer
from datetime import date
import json


CARE_PLAN_TEMPLATE = """
You are an AI assistant designed to update and improve elder care plans by incorporating the most recent relevant review information. Please provide an improved version of the care plan by following these steps:

## CRITICAL INSTRUCTIONS:
- DO NOT MOVE ANY EXISTING INFORMATION BETWEEN SECTIONS UNDER ANY CIRCUMSTANCES.
- ALWAYS integrate the most recent review into the appropriate section(s) of the care plan.
- DO NOT suggest moving information to other sections.
- Each piece of existing information must remain exactly where it was in the original subplan.


<INSTRUCTIONS>

1. Do not move existing content between sections under any circumstances.
2. Review Integration:
   a. Carefully read through the "Reviews" section
   b. Identify the most recent review by following these steps:
      - Convert all dates to a standardized format (DD-MM-YYYY) for accurate comparison
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
OUTPUT
"""

# i. Clearly mark any new additions with [NEW] tags

# Note: Do not include a "Reviews" section in the output. The review information should be integrated into the appropriate sections above.

CARE_PLAN_TEMPLATE2 = """
# Enhanced Care Plan Update Prompt

You are an AI assistant designed to update elder care plans by incorporating the most recent review information. Your primary tasks are to accurately identify the most recent review(s) and determine if any updates are necessary.

## CRITICAL INSTRUCTIONS:
- ALWAYS select the most recent review(s) based on the date.
- If multiple reviews exist for the most recent date, consider ALL of them.
- If ANY of the most recent reviews state "Care plan reviewed, no changes", "No changes of this care plan, care plan ongoing" or any similar phrasing, still consider the other reviews from the same date for potential updates.
- Only update the care plan if the most recent review(s) contain new information.
- When updating, DO NOT MOVE ANY EXISTING INFORMATION BETWEEN SECTIONS.
- DO NOT add information to the "Assessed current situations" section unless explicitly mentioned in the most recent review(s).
- Each piece of existing information must remain in its original location.

<INSTRUCTIONS>

1. Review Selection:
   a. Read through the "Reviews" section carefully.
   b. Identify the most recent review(s) using this method:
      - Compare years first (e.g., 24 for 2024) with current year (date/month/year): {date}
      - If years are the same, compare months (01-12)
      - If months are the same, compare days (01-31)
      - Select ALL reviews with the latest date
   c. DOUBLE CHECK your selection by comparing it to all other dates

2. Review Integration:
   a. If ALL of the most recent reviews state "Care plan reviewed, no changes", "No changes of this care plan, care plan ongoing" or similar, DO NOT make any changes to the care plan.
   b. If ANY of the most recent reviews contain new information:
      - Rewrite the selected review(s) concisely, omitting reviewer info
      - Maintain all relevant information from the original entries
      - Determine which information from the review(s) needs to be added to the care plan
      - Choose the most appropriate section(s) for integration:
        - Care needs
        - Outcome/goal
        - Description of care actions
      - Insert the relevant information from the review(s) into the chosen section(s)
      - Ensure the new information flows logically with existing content
      - Mark new additions with [NEW] tags
      - IMPORTANT: When adding new information, provide clear, detailed sentences that fully explain the new instructions or observations. Do not use brief phrases or incomplete sentences.
   c. DO NOT add information to the "Assessed current situations" section unless explicitly mentioned in the most recent review(s)

3. Verification:
   a. Confirm you've correctly handled all of the most recent reviews
   b. If changes were made, verify that the information from the review(s) has actually been added to the relevant sections
   c. Verify no existing content has been moved between sections
   d. Ensure all original content remains in place

4. Standardization:
   - Ensure clarity, professional presentation, and correct grammar throughout

</INSTRUCTIONS>

CRITICAL: Correctly identifying the most recent review(s) AND determining whether updates are necessary are your primary tasks.

EXAMPLES:

Example 1: No changes required
Most recent review: "10/06/24 John Doe - Care plan reviewed, no changes"

In this case, DO NOT make any changes to the care plan. The output should state that no changes were made due to the review content.

Example 2: Updates required
Most recent review: "05/06/24 Jane Smith - Patient shows improved mobility, can now walk short distances with a walker"

In this case, update the relevant sections of the care plan:
Care needs: [NEW] Patient has shown significant improvement in mobility. They are now able to walk short distances with the assistance of a walker, which represents a notable progress in their physical capabilities.
Description of care actions: [NEW] Encourage and assist the patient with short walking exercises using a walker to maintain and improve mobility. Staff should supervise these walking sessions, ensuring the patient's safety and gradually increasing the distance as tolerated. Document the patient's progress after each session.

Example 3: Most recent review with no substantial changes
Reviews:
10/06/24 Mike Johnson - Continuing with current care plan, patient stable
05/06/24 Jane Smith - Patient shows improved mobility, can now walk short distances with a walker

In this example, even though 10/06/24 is the most recent review, it doesn't contain new information for the care plan. Therefore, no changes should be made to the care plan.

Example 4: Multiple reviews on the same date
Most recent reviews:
"25/06/24 John Doe - Blood test results normal, continue monitoring"
"25/06/24 Jane Smith - Patient shows improved appetite, increase portion sizes"

In this case, consider both reviews and update the care plan accordingly:
Care needs: [NEW] Patient's recent blood test results have come back normal, indicating stable health conditions. Additionally, the patient has demonstrated an improved appetite, suggesting a positive change in their nutritional status.
Description of care actions: [NEW] Continue regular monitoring of the patient's health status, including periodic blood tests as scheduled by the physician. In response to the improved appetite, increase portion sizes for all meals. Monitor and document the patient's food intake, ensuring they are receiving adequate nutrition to support their improved appetite.

Example 5: One review indicates no changes, but another has new information
Most recent reviews:
"10/06/24 Mike Johnson - Care plan reviewed, no changes"
"10/06/24 Sarah Brown - Patient now able to walk with a cane, physiotherapy to continue"

In this case, update the care plan based on Sarah Brown's review:
Care needs: [NEW] Patient has demonstrated significant progress in mobility and can now walk with the assistance of a cane. This represents an improvement from their previous mobility status and indicates a positive response to ongoing physiotherapy.
Description of care actions: [NEW] Continue regular physiotherapy sessions to support and further improve the patient's mobility with cane use. Staff should encourage the patient to use the cane when walking and provide supervision as needed to ensure safety. Monitor and document the patient's progress, including the distance walked and any challenges encountered.

Example 6: Detailed integration of multiple reviews
Most recent reviews:
"25/06/24 Dr. Smith - Blood test results for bruising have come back normal. Advised to closely monitor the skin."
"25/06/24 Dietitian Jones - Discharged patient. Continue with the same dietary plan but check Fresubin instructions and offer as shorts."

In this case, update the care plan as follows:

Care needs:
[NEW] Teresa's blood test results related to her recent bruising have returned normal. However, due to her history of bruising, her skin condition still requires vigilant monitoring to ensure early detection of any changes or new bruising.
[NEW] Teresa has been discharged by the dietitian, who recommends continuing the current dietary plan. A modification has been suggested in the administration of Fresubin, a nutritional supplement, to potentially improve its effectiveness and Teresa's tolerance.

Description of care actions:
[NEW] Staff must continue to closely monitor Teresa's skin for any signs of bruising or changes in skin condition. This includes conducting thorough skin checks during personal care routines and immediately reporting any new bruises or skin changes to the nurse in charge. Even though recent blood test results were normal, this vigilant monitoring is necessary due to Teresa's history of bruising.
[NEW] When administering Fresubin to Teresa, staff should carefully review the product instructions and offer it as "shorts". This means providing the Fresubin in smaller, more frequent doses throughout the day rather than in larger amounts. For example, if Teresa was previously receiving 200ml twice a day, consider offering 100ml four times a day, adjusting as per dietitian's specific instructions. This change in administration method may help improve Teresa's intake and digestion of the supplement. Staff should monitor and document Teresa's response to this new administration method, including any changes in her tolerance or overall intake.

OUTPUT FORMAT:
[SECTION_NAME]

Assessed current situations:
[Updated content ONLY if explicitly mentioned in the most recent review(s)]

Care needs:
[Updated content if applicable, with detailed explanations]

Outcome/goal:
[Updated content if applicable, with detailed explanations]

Description of care actions:
[Updated content if applicable, with detailed explanations]

Reviews:
[Original review content, unchanged]

Most Recent Review(s):
Date: [Date of most recent review(s)]
Content: [Content of most recent review(s)]

Reasoning:
[Explain why these are the most recent reviews. If no changes were made due to the review content, explain this. If changes were made, explain in detail how you integrated the review information into the care plan sections, including why certain sections were chosen for the new information.]

INPUT:
{plan_subsection}

OUTPUT:
[Updated care plan with correct integration of the most recent review information into the relevant sections, using detailed and clear sentences to explain new instructions or observations. If no changes were made, provide a detailed explanation of why.]
"""
# Most Recent Review Selected:
# [Date and content of the most recent review you selected]

# Reasoning for Review Selection:
# [Briefly explain why you selected this as the most recent review]

global standardize_care_plan_llm
standardize_care_plan_llm=GeminiInitializer()


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
    formatted_date = "17/07/2024" #today.strftime("%d/%m/%y")
    prompt = CARE_PLAN_TEMPLATE2.format(plan_subsection=text, date = formatted_date)
    print("-----------------"*5)
    response = standardize_care_plan_llm.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
    
    print(f"Review added : {response}")
    response = str(response).split("Most Recent Review:")[0]
    return response
 
 


