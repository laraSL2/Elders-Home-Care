from gemini_initializer import GeminiInitializer
from datetime import date

# <TASK 1: Decision Making>
# </TASK 1: Decision Making>
# <TASK 2: Enhancement>
# </TASK 2: Enhancement>

CARE_PLAN_TEMPLATE4 = """
You are an expert in elder care plan documentation. Your task is to analyze, compare, and enhance the quality of two given subplans. Based on the comparison, decide whether to combine them into one subplan or maintain them as separate subplans. Provide a clear and detailed explanation of your reasoning and changes made. Follow these steps:


Instructions:
Task-01
   In this task, you will analyze and compare the provided subplans to determine if they should be combined into one comprehensive plan or maintained as separate subplans. This involves understanding the care needs, goals, and actions described in each subplan.

   1. Input Analysis:
      - Extract key information from the given subplans.

   2. Comparison:
      - Compare the care needs.
      - Compare the goals and outcomes of both subplans.
      - Compare the description of care actions.
      - Compare the reviews and their content.
      - Determine if there are overlapping or distinct areas in the care actions, goals, care needs, assessed current situations, and reviews.

   Examples:
      - Care Needs Comparison: "Subplan A mentions the need for cognitive stimulation, while Subplan B highlights the requirement for regular medication administration."
      - Goals and Outcomes Comparison: "Both subplans aim to improve the resident's quality of life, but one focuses on communication and the other on medication adherence."
      - Care Actions Comparison: "Subplan A includes actions like engaging in conversation, while Subplan B involves administering medications."
      - Reviews Comparison: "Subplan A's reviews mention the resident's ability to communicate, whereas Subplan B's reviews focus on medication management."

   3. Decision Making:
      - Criteria for Combination: Determine if the subplans can be combined into one based on the overlap in each section (care actions, goals, care needs, assessed current situations, reviews).
      - Criteria for Separation: If they address distinct areas of care, maintain them as separate subplans.

   Examples:
      - Combined Decision: "Since both subplans aim to improve the resident's overall well-being and involve daily interactions, they can be combined into a single comprehensive care plan."
      - Separate Decision: "The subplans address distinct areas (communication and medication) and should remain separate to ensure focused care."


Task-02
   In this task, you will enhance the clarity, coherence, and professionalism of the subplans based on the decision made in Task 1. This includes fixing grammar and spelling mistakes, enhancing content accuracy, and formatting the text for better readability.


   4. Enhancement:
      - Rewrite the combined or individual subplans to improve clarity and coherence.
      - Ensure the language is consistent and professional.
      - For each subplan (or the combined plan if applicable):
        a. Identify and remove any redundant or outdated information.
        b. Organize the content into clear, logical sections.
        c. Ensure consistent formatting and use of terminology.
        d. Highlight any discrepancies in patient information (e.g., different names used).

   Examples:
      - Original: "The resident can communicate but sometimes gets confused."
      - Enhanced: "The resident is able to communicate effectively, although they occasionally experience confusion."

   5. Fix Grammar and Spelling Mistakes:
      - Correct grammatical errors while maintaining the original meaning.
      - Fix spelling mistakes and typos.

   Examples:
      - Original: "pt agitated, gave meds"
      - Enhanced: "The patient was agitated; therefore, medication was administered."

   6. Enhance Content Accuracy and Completeness:
      - Ensure logical consistency and chronological order of events.
      - Infer and include implied information based on context.
      - Remove redundancies while preserving all relevant details.

   Examples:
      - Original: "fell outta bed last nite"
      - Enhanced: "During the night, the resident fell out of bed. Staff immediately assessed for injuries and implemented necessary safety protocols."

   7. Reformat and Expand Sentences:
      - Organize information in a clear, chronological order.
      - Include relevant details about the care session, resident's state, and caregiver actions.
      - Enhance the note to provide a comprehensive view of the care provided.

   Examples:
      - Original: "The resident talked with staff."
      - Enhanced: "The resident engaged in a meaningful conversation with the staff, discussing their favorite pastimes and current interests, which provided cognitive stimulation."

   8. Output a Concise, Detailed Paragraph:
      - Combine all improved information into a single, well-structured paragraph.
      - Ensure the paragraph flows logically and provides a complete picture of the care session.

   Examples:
      - Enhanced Paragraph: "The resident was able to communicate effectively with the staff, discussing their favorite activities and expressing their needs clearly. During the medication administration, the resident followed instructions well and experienced no side effects. Staff ensured their glasses were clean and their ears were checked for wax, facilitating better communication."

   9. Output Generation:
      - Provide a detailed explanation of the changes made.
      - Ensure that existing content remains in its original sections without being moved or relocated. You must strictly adhere to this instruction.



Input Subplans:

Subplan A:
{Subplan_A}

Subplan B:
{Subplan_B}

Your goal is to enhance the quality and usability of the care plan(s) while maintaining all relevant and current information.

OUTPUT_FORMAT:

- If the decision is to keep the subplans separate:

   Enhanced Subplan A:
   [Updated content for Subplan A]

   Enhanced Subplan B:
   [Updated content for Subplan B]

- If the decision is to combine the subplans:

   Combined Enhanced Subplan: 
   [Title]
   
   Assessed Current Situation:
   [Combined and enhanced assessment of the current situation from both subplans]

   
   Care Needs:
   [Combined and enhanced care needs from both subplans]

   Outcomes and Goals:
   [Combined and enhanced goals and outcomes from both subplans]

   Description of Care Actions:
   [Combined and enhanced care actions from both subplans]

   Reviews:
   [Combined and enhanced reviews from both subplans]

Reasoning and Changes: (Insert detailed reasoning and changes made)
  - Decision: 
  - Reasoning:

  - General Changes:
  - Consistency and Clarity:
  - Capitalization and Punctuation:
  - Sentence Structure:
  - Specific Changes:
"""





PLAN = """
You are an expert in elder care plan documentation. Your task is to analyze, compare, and enhance the quality of two given subplans. Based on the comparison, decide whether to combine them into one subplan or maintain them as separate subplans. Provide a clear and detailed explanation of your reasoning and changes made. Follow these steps:


Instructions:
Task-01
   In this task, you will analyze and compare the provided subplans to determine if they should be combined into one comprehensive plan or maintained as separate subplans. This involves understanding the care needs, goals, and actions described in each subplan.

   1. Input Analysis:
      - Extract key information from the given subplans.

   2. Comparison:
      - Compare the care needs.
      - Compare the goals and outcomes of both subplans.
      - Compare the description of care actions.
      - Compare the reviews and their content.
      - Determine if there are overlapping or distinct areas in the care actions, goals, care needs, assessed current situations, and reviews.

   Examples:
      - Care Needs Comparison: "Subplan A mentions the need for cognitive stimulation, while Subplan B highlights the requirement for regular medication administration."
      - Goals and Outcomes Comparison: "Both subplans aim to improve the resident's quality of life, but one focuses on communication and the other on medication adherence."
      - Care Actions Comparison: "Subplan A includes actions like engaging in conversation, while Subplan B involves administering medications."
      - Reviews Comparison: "Subplan A's reviews mention the resident's ability to communicate, whereas Subplan B's reviews focus on medication management."

   3. Decision Making:
      - Criteria for Combination: Determine if the subplans can be combined into one based on the overlap in each section (care actions, goals, care needs, assessed current situations, reviews).
      - Criteria for Separation: If they address distinct areas of care, maintain them as separate subplans.

   Examples:
      - Combined Decision: "Since both subplans aim to improve the resident's overall well-being and involve daily interactions, they can be combined into a single comprehensive care plan."
      - Separate Decision: "The subplans address distinct areas (communication and medication) and should remain separate to ensure focused care."


Task-02
   In this task, you will enhance the clarity, coherence, and professionalism of the subplans based on the decision made in Task 1. This includes fixing grammar and spelling mistakes, enhancing content accuracy, and formatting the text for better readability.


   4. Enhancement:
      - Rewrite the combined or individual subplans to improve clarity and coherence.
      - Ensure the language is consistent and professional.
      - For each subplan (or the combined plan if applicable):
        a. Identify and remove any redundant or outdated information.
        b. Organize the content into clear, logical sections.
        c. Ensure consistent formatting and use of terminology.
        d. Highlight any discrepancies in patient information (e.g., different names used).

   Examples:
      - Original: "The resident can communicate but sometimes gets confused."
      - Enhanced: "The resident is able to communicate effectively, although they occasionally experience confusion."

   5. Fix Grammar and Spelling Mistakes:
      - Correct grammatical errors while maintaining the original meaning.
      - Fix spelling mistakes and typos.

   Examples:
      - Original: "pt agitated, gave meds"
      - Enhanced: "The patient was agitated; therefore, medication was administered."

   6. Enhance Content Accuracy and Completeness:
      - Ensure logical consistency and chronological order of events.
      - Infer and include implied information based on context.
      - Remove redundancies while preserving all relevant details.

   Examples:
      - Original: "fell outta bed last nite"
      - Enhanced: "During the night, the resident fell out of bed. Staff immediately assessed for injuries and implemented necessary safety protocols."

   7. Reformat and Expand Sentences:
      - Organize information in a clear, chronological order.
      - Include relevant details about the care session, resident's state, and caregiver actions.
      - Enhance the note to provide a comprehensive view of the care provided.

   Examples:
      - Original: "The resident talked with staff."
      - Enhanced: "The resident engaged in a meaningful conversation with the staff, discussing their favorite pastimes and current interests, which provided cognitive stimulation."

   8. Output a Concise, Detailed Paragraph:
      - Combine all improved information into a single, well-structured paragraph.
      - Ensure the paragraph flows logically and provides a complete picture of the care session.

   Examples:
      - Enhanced Paragraph: "The resident was able to communicate effectively with the staff, discussing their favorite activities and expressing their needs clearly. During the medication administration, the resident followed instructions well and experienced no side effects. Staff ensured their glasses were clean and their ears were checked for wax, facilitating better communication."

   9. Output Generation:
      - Provide a detailed explanation of the changes made.
      - Ensure that existing content remains in its original sections without being moved or relocated. You must strictly adhere to this instruction.



Input Subplans:

Subplan A:
{Subplan_A}

Subplan B:
{Subplan_B}

Your goal is to enhance the quality and usability of the care plan(s) while maintaining all relevant and current information.

OUTPUT_FORMAT:

Enhanced Subplan(s):
[Updated content]

Reasoning and Changes: (Insert detailed reasoning and changes made)
  - Decision: 
  - Reasoning:

  - General Changes:
  - Consistency and Clarity:
  - Capitalization and Punctuation:
  - Sentence Structure:
  - Specific Changes:
"""


CARE_PLAN_TEMPLATE2 = """
You are an expert in elder care plan documentation. Your task is to analyze, compare, and enhance the quality of two given subplans. Based on the comparison, decide whether to combine them into one subplan or maintain them as separate subplans. Provide a clear and detailed explanation of your reasoning and changes made. Follow these steps:


Instructions:
Task-01
   In this task, you will analyze and compare the provided subplans to determine if they should be combined into one comprehensive plan or maintained as separate subplans. This involves understanding the care needs, goals, and actions described in each subplan.

   1. Input Analysis:
      - Extract key information from the given subplans.

   2. Comparison:
      - Compare the care needs.
      - Compare the goals and outcomes of both subplans.
      - Compare the description of care actions.
      - Compare the reviews and their content.
      - Determine if there are overlapping or distinct areas in the care actions, goals, care needs, assessed current situations, and reviews.

   Examples:
      - Care Needs Comparison: "Subplan A mentions the need for cognitive stimulation, while Subplan B highlights the requirement for regular medication administration."
      - Goals and Outcomes Comparison: "Both subplans aim to improve the resident's quality of life, but one focuses on communication and the other on medication adherence."
      - Care Actions Comparison: "Subplan A includes actions like engaging in conversation, while Subplan B involves administering medications."
      - Reviews Comparison: "Subplan A's reviews mention the resident's ability to communicate, whereas Subplan B's reviews focus on medication management."

   3. Decision Making:
      - Criteria for Combination: Determine if the subplans can be combined into one based on the overlap in each section (care actions, goals, care needs, assessed current situations, reviews).
      - Criteria for Separation: If they address distinct areas of care, maintain them as separate subplans.

   Examples:
      - Combined Decision: "Since both subplans aim to improve the resident's overall well-being and involve daily interactions, they can be combined into a single comprehensive care plan."
      - Separate Decision: "The subplans address distinct areas (communication and medication) and should remain separate to ensure focused care."


Task-02
   In this task, you will enhance the clarity, coherence, and professionalism of the subplans based on the decision made in Task 1. This includes fixing grammar and spelling mistakes, enhancing content accuracy, and formatting the text for better readability.


   4. Enhancement:
      - Rewrite the combined or individual subplans to improve clarity and coherence.
      - Ensure the language is consistent and professional.
      - For each subplan (or the combined plan if applicable):
        a. Identify and remove any redundant or outdated information.
        b. Organize the content into clear, logical sections.
        c. Ensure consistent formatting and use of terminology.
        d. Highlight any discrepancies in patient information (e.g., different names used).

   Examples:
      - Original: "The resident can communicate but sometimes gets confused."
      - Enhanced: "The resident is able to communicate effectively, although they occasionally experience confusion."

   5. Fix Grammar and Spelling Mistakes:
      - Correct grammatical errors while maintaining the original meaning.
      - Fix spelling mistakes and typos.

   Examples:
      - Original: "pt agitated, gave meds"
      - Enhanced: "The patient was agitated; therefore, medication was administered."

   6. Enhance Content Accuracy and Completeness:
      - Ensure logical consistency and chronological order of events.
      - Infer and include implied information based on context.
      - Remove redundancies while preserving all relevant details.

   Examples:
      - Original: "fell outta bed last nite"
      - Enhanced: "During the night, the resident fell out of bed. Staff immediately assessed for injuries and implemented necessary safety protocols."

   7. Reformat and Expand Sentences:
      - Organize information in a clear, chronological order.
      - Include relevant details about the care session, resident's state, and caregiver actions.
      - Enhance the note to provide a comprehensive view of the care provided.

   Examples:
      - Original: "The resident talked with staff."
      - Enhanced: "The resident engaged in a meaningful conversation with the staff, discussing their favorite pastimes and current interests, which provided cognitive stimulation."

   8. Output a Concise, Detailed Paragraph:
      - Combine all improved information into a single, well-structured paragraph.
      - Ensure the paragraph flows logically and provides a complete picture of the care session.

   Examples:
      - Enhanced Paragraph: "The resident was able to communicate effectively with the staff, discussing their favorite activities and expressing their needs clearly. During the medication administration, the resident followed instructions well and experienced no side effects. Staff ensured their glasses were clean and their ears were checked for wax, facilitating better communication."

   9. Output Generation:
      - Provide a detailed explanation of the changes made.
      - Ensure that existing content remains in its original sections without being moved or relocated. You must strictly adhere to this instruction.



Input Subplans:

Subplan A:
{Subplan_A}

Subplan B:
{Subplan_B}

Your goal is to enhance the quality and usability of the care plan(s) while maintaining all relevant and current information.

OUTPUT_FORMAT:

   - If the decision is to keep the subplans separate:

      Enhanced Subplan A:
      [Updated content for Subplan A]

      Enhanced Subplan B:
      [Updated content for Subplan B]

   - If the decision is to combine the subplans:

      Combined Enhanced Subplan: 
         [Title]

      Assessed Current Situation:
         [Combined and enhanced assessment of the current situation from both subplans]


      Care Needs:
         [Combined and enhanced care needs from both subplans]

      Outcomes and Goals:
         [Combined and enhanced goals and outcomes from both subplans]

      Description of Care Actions:
         [Combined and enhanced care actions from both subplans]
            
      Reviews:
         [Combined reviews from both subplans, organized in chronological order from most recent to oldest. Do not use review content to update the plan.]

      
   Reasoning and Changes: (Insert detailed reasoning and changes made)
     - Decision: 
     - Reasoning:

     - General Changes:
     - Consistency and Clarity:
     - Capitalization and Punctuation:
     - Sentence Structure:
     - Specific Changes:
     
IMPORTANT: The content in the Reviews section is for reference only and should not be used to directly modify the care plan. Any changes to the care plan based on reviews should be made through a formal update process.
 
FINAL_PLAN:
"""






global standardize_care_plan_llm
standardize_care_plan_llm=GeminiInitializer()

def final_care_plan(sub_plan_1, sub_plan_2):
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
    prompt = CARE_PLAN_TEMPLATE.format(Subplan_A=sub_plan_1, Subplan_B=sub_plan_2 )
    print("-----------------"*5)
    response = standardize_care_plan_llm.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
    print(response)
    
    return response



sub_plan_1 = """
 Emotional support

 Assessed current situations

 Care needs

Teresa can be very anxious as evidenced by her behaviour of saying "please don't hurt me""please
GOD help me", but she is easily reassured this especially happens when being supported that
requires touching her like personal care and or toilet needs.
She always ask "where am I?""when am I going home?" she can be answered that she is at Larchfield
House in Maidenhead and we are looking after her and she will settle.
Teresa likes sharing stories about her life, it makes her happy.
Teresa likes her own company in the room when she watches TV. However, she loves to be in a
common area and chatting with others.
Teresa is very sociable and inquisitive person and is able to talk about different topics.
I tried to call Lesley, Teresa's daughter in order to get her consent for her bedroom to be closed while
she is not there with the purpose to protect her belongings from others service users which are
wandering around the community. After a call back, she has gave her consent on the 6.2.2023.

 Outcome/goal
For Teresa to feel supported in all aspects which includes emotional support.
To make Teresa feel safe and comfortable at Larchfield House

 Description of care actions
When supporting Teresa with personal care which includes toileting and hoisting, she requires 2
staff and should always include at least 1 female.
Staff should consistently reassure her and explain to her the purpose of the support and what she
has to do every step, only one staff to lead and talk so as to avoid confusion.
Staff to spend time with Teresa to talk about her interests.
Staff to document all emotional support given to Teresa on PCS.

 Reviews
09/06/24 Babu Joseph - Staff continuous to reassure Teresa, care plan ongoing
16/04/24 Barbara Mpofu - Staff continue to support and reassure Teresa when she is emotional
and confused.
12/03/24 Jeanine Generoso - There are times that Teresa is sociable, but she can also be very
anxious. Staff to provide emotional support and reassurance Teresa at all times. Care plan in place
and on going.
07/02/24 Barbara Mpofu - Teresa can at times be anxious, staff continue to support and reassure
her. Care plan ongoing.

06/01/24 Vipinkumar Chakkungapady - Teresa needs constant reassurance and emotional support when she became anxious
and confused. The care plan is ongoing.
20/12/23 Babu Joseph - Staff continuous to support and reassure her, no changes, care plan
ongoing
22/11/23 Shital Magar - Teresa is very sociable and inquisitive person and is able to talk about
different topics.
05/10/23 Vipinkumar Chakkungapady - Teresa needs constant reassurance and emotional support
when she became anxious and confused. The care plan is ongoing.
05/09/23 Jojo Serrana - Staff to continuously support Teresa when she is emotional and confuse.
Staff to continuously provide reassurance when she is emotionally down.
30/08/23 Shital Magar - Teresa needs continues reassurance and emotional support,care plan
ongoing.
20/07/23 Babu Joseph - Staff continuous to support and reassure Theresa, care plan ongoing
"""


sub_plan_2 = """
 Finance (LPA for Finance and Property only)

 Assessed current situations

 Care needs

Teresa has LPA for Finances and and Property only and it is her Daughter Lesley.
Anything Teresa requires to support her with Holistic care, we call Lesley.
*Received a HM Revenue & Customs letter dated :28 sep 2023.
Teresa is notin receipt of Pension Credit or any credit
Teresa had a gold ring which started falling off, the ring is handed over to Ullka to keep in the safe
locker on 17/04/24, but Lesley Kirkuk Daughter of Teresa took it with her on 24.04.24

 Outcome/goal
To support and provide Teresa's basic needs
To ensure that Teresa's finances is managed well with the help of her daughter
To protect Teresa from financial abuse

 Description of care actions
Care Staff especially the Key Worker should keep an eye on things Teresa needed and to call her
Daughter Lesley.
Care Staff to record on the property lists form every time Lesley brings in properties likes clothing
and or other non consumable things.
Care staff to report to Teresa's NOK with LPA if there are any concerns with her finances.

 Reviews
09/06/24 Babu Joseph - No changes of this care plan, care plan ongoing
24/04/24 Henry De Sousa - Teresa had a gold ring which started falling off, the ring is handed over
to Ullka to keep in the safe locker on 17/04/24, but Lesley Kirkuk Daughter of Teresa took it with
her on 24.04.24
17/04/24 Henry De Sousa - Teresa had a gold ring which she started falling off, the ring is handed
over to Ullka to keep in the safe locker on 17/04/24, will inform the Family as well.
16/04/24 Barbara Mpofu - Teresa's daughter continues to manage all her finances. Care plan
remains valid and ongoing.
12/03/24 Jeanine Generoso - Lesley, Teresa's daughter has the LPA for her Finances and Property.
Care plan in place and on going.
07/02/24 Barbara Mpofu - Teresa's daughter continues to manage all her finances. Care plan
remains valid and ongoing.
06/01/24 Vipinkumar Chakkungapady - Teresa's daughter Lesley, holds LPA to manage her finances. The care plan is ongoing.

20/12/23 Babu Joseph - Teresa's daughter still managing the finances for her, no changes, care plan
ongoing
22/11/23 Shital Magar - Daughter Lesley, holds LPA to manage Teresa's finances
07/10/23 Henry De Sousa - Received a HM Revenue & Customs letter dated :28 sep 2023.
05/10/23 Vipinkumar Chakkungapady - Teresa's daughter Lesley, holds LPA to manage her finances. The care plan is
ongoing.
05/09/23 Jojo Serrana - Daughter Lesley, holds LPA to manage Teresa's finances.
"""

final_care_plan(sub_plan_1, sub_plan_2)