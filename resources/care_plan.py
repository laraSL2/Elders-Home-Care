from typing import List, Dict
import time
from datetime import datetime
from gemini_initializer import GeminiInitializer
from datetime import date

CARE_PLAN_TEMPLATE2 = """
# Expert Care Plan Documentation Analysis, Review Integration, and Enhancement

As an expert in elder care plan documentation, your task is to update each subplan with the latest review, enhance the quality of the provided subplans, analyze similarities, and potentially combine subplans, all while strictly maintaining the original structure and content placement. Follow these steps meticulously:

## CRITICAL INSTRUCTIONS:
- DO NOT MOVE ANY EXISTING INFORMATION BETWEEN SECTIONS UNDER ANY CIRCUMSTANCES.
- ALWAYS integrate the most recent review into the appropriate section(s) of the care plan.
- DO NOT suggest moving information to other sections or plans.
- Each piece of existing information must remain exactly where it was in the original subplan.

## Task 1: Review Integration

For each subplan:

1. Review Integration:
   a. Carefully read through the "Reviews" section.
   b. Identify the most recent review by finding the latest date in the format DD/MM/YY.
   c. Analyze and summarize the content of the most recent review, focusing on any changes or new information about the elder's condition, care, or medication.
   d. Determine which of the following sections the new information best fits into:
      - Assessed Current Situation
      - Care Needs
      - Outcomes and Goals
      - Description of Care Actions
   e. Rewrite the selected review as a clear, concise, and professional update, avoiding caregiver names or irrelevant details.
   f. Insert this update into the most appropriate section(s) identified in step d.
   g. Ensure the new information flows logically with the existing content in the section(s).
   h. Clearly mark any new additions with [NEW] tags.
   i. If the review doesn't fit clearly into any section, add it to the most relevant section based on its content.

2. After updating with the review, verify that all original content remains in its original place and that the new review information has been added.

## Task 2: Text Quality Enhancement and Expansion

For each subplan:

1. Text Quality Enhancement:
   - Improve clarity and coherence of the content within each section.
   - Ensure consistent and professional language throughout.
   - Fix any grammar and spelling mistakes.
   - Enhance readability by refining sentence structure and word choice.

2. Content Expansion:
   - Expand on existing information to provide more comprehensive details, where appropriate.
   - Add relevant context or explanations to make the information more thorough and understandable.
   - Ensure all expansions remain within the same section as the original information.
   - If a section was empty in the original, it must remain empty. Do not add new information to empty sections.

3. Maintain Section Integrity:
   - Do not move any information between sections: Assessed Current Situation, Care Needs, Outcomes and Goals, Description of Care Actions.
   - Do not suggest moving information to other sections or plans.

4. Duplication Management:
   - Remove exact duplicates of information within the same section.
   - Preserve similar information that may provide additional context or nuance, even if it appears redundant.

5. Chronological Ordering:
   - Within each section, ensure events or information are presented in a logical, chronological order where applicable.

## Task 3: Comprehensive Analysis and Similarity Assessment

After enhancing each individual subplan:

1. Similarity Comparison:
   - Compare each subplan with every other subplan for similarities in all components.
   - Use the provided information in {combine_instructions} to guide your decision on which subsections can be combined.
   - Identify groups of subplans with high similarity across multiple components.
   - Consider the overall context and purpose of each subplan, not just textual similarity.

2. Decision Making:
   - Based on the {combine_instructions}, determine whether any subplans should be combined or if all should remain separate.
   - If combination is allowed and beneficial, identify groups of subplans that are highly similar and would benefit from combination.
   - Maintain unique subplans as separate.

3. Combination Process (if applicable and allowed by {combine_instructions}):
   For each group of subplans to be combined:
   a. Create a new, comprehensive subplan that incorporates all unique elements from the original subplans.
   b. Strictly maintain the original structure of the subplans (Assessed Current Situation, Care Needs, Outcomes and Goals, Description of Care Actions, and Reviews).
   c. Ensure that information from each section is merged only into the corresponding section of the combined subplan.
   d. Do not move any information between sections during this process.
   e. Preserve all unique information from each original subplan, even if it seems redundant.

## Input:
Subplans: {subplans}
Combination Instructions: {combine_instructions}

## Output Format:

### Enhanced Care Plans:

[For each resulting subplan (whether original or combined), use the following format:]

Subplan [X] (Original) or Combined Subplan [Y] (from original subplans [A], [B], [C], ...):
   Title: [Provide a concise title for the subplan]

   Assessed Current Situation:
      [Enhanced assessment of the current situation, strictly preserving all original information and placement. Include any new review information marked with [NEW] tags if applicable.]

   Care Needs:
      [Enhanced care needs, strictly preserving all original information and placement. Include any new review information marked with [NEW] tags if applicable.]

   Outcomes and Goals:
      [Enhanced goals and outcomes, strictly preserving all original information and placement. Include any new review information marked with [NEW] tags if applicable.]

   Description of Care Actions:
      [Enhanced care actions, strictly preserving all original information and placement. Include any new review information marked with [NEW] tags if applicable.]

   Reviews:
      [Reviews organized in chronological order from most recent to oldest. Ensure the most recent review has been integrated into the appropriate section(s) above.]

### Similarity Analysis Summary:
[Provide a detailed summary of the similarity analysis, explaining which subplans were found to be highly similar and whether they will be combined based on the {combine_instructions}. Explain your reasoning for each decision.]

### Reasoning and Changes:
   - Review Integration: [Explain how the most recent review was interpreted and integrated into the care plan, specifying which section(s) it was added to]
   - Decisions: [Explain which subplans were combined, if any, and which remained separate]
   - Reasoning: [Provide detailed reasoning for the decisions made]
   - General Enhancements: [Describe overall enhancements made across all subplans, emphasizing that no information was moved between sections]
   - Specific Enhancements: [List specific significant enhancements made to each subplan]

### Final Plan Summary:
   [Provide a comprehensive summary of the final result, including:
 - The number of original subplans
 - The number of resulting subplans after analysis and potential combination
 - A brief overview of any reorganization (if applicable)
 - Any key observations or recommendations based on the analysis]

### Information Preservation Check:
   [Confirm that all original information has been preserved in its original sections. Confirm that sections that were originally empty have remained empty, except for new review information. Verify that the most recent review has been integrated into the appropriate section(s).]

### Quality Assurance Check:
   [Provide a brief assessment of the overall quality of the enhanced care plans, addressing:
 - Clarity and coherence of information
 - Completeness of care needs and actions
 - Logical flow within each section
 - Consistency of terminology and phrasing
 - Strict adherence to the original structure and content placement
 - Proper integration of the most recent review
 - Any areas that may require further clarification or expansion]
"""


CARE_PLAN_TEMPLATE3 = """
# Comprehensive Multi-Subplan Care Plan Update and Enhancement

You are an AI assistant specializing in elder care plan documentation. Your task is to update, enhance, and standardize multiple care plan subplans in a single, comprehensive process. Follow these instructions meticulously to ensure the highest quality outcome.

## CRITICAL INSTRUCTIONS (Apply at all times):
- NEVER move any information between subplans or between sections within a subplan.
- Maintain the exact original structure of each subplan.
- If a section was empty in the original subplan, it MUST remain empty.
- Preserve ALL information, even if it seems outdated or redundant.
- Always use the provided current date to identify the most recent reviews.
- Include ALL reviews from the most recent date, even if they appear to be duplicates.
- Format the Assessed Current Situations, Care Needs, Outcomes and Goals, and Description of Care Actions sections in a point-by-point format.
- Ensure impeccable grammar, spelling, and clarity throughout the document.
- DO NOT use [NEW] tags.
- Present all reviews in reverse chronological order, with the most recent at the top.
- Maintain consistent capitalization and punctuation throughout the document.
- Expand concise sentences into more detailed, professional descriptions without adding any new information.
- Replace "Historical Information" with "Comprehensive Medical Background".
- Never add or fabricate information not present in the original content.

## Input:
- Subplans: {subplans}
- Current Date: {current_date}

## Process Overview:
1. Review Identification and Update
2. Content Enhancement and Information Preservation
3. Standardization and Proofreading
4. Review Chronology Correction
5. Final Output Generation

## Detailed Instructions:


### 1. Review Identification and Update
For each subplan:
a. Identify the most recent review(s) by comparing dates to the provided current date: {current_date}.
b. Use this method to compare dates:
   - Compare years first (e.g., 24 for 2024)
   - If years are the same, compare months (01-12)
   - If months are the same, compare days (01-31)
c. Select ALL reviews with the latest date, even if there are multiple entries for the same date.
d. If multiple reviews exist for the most recent date, include ALL of them in your update.
e. Update the care plan with new information from the most recent review(s).
f. Integrate new information into appropriate sections (Care Needs, Outcome/Goal, Description of Care Actions).
g. Mark new additions with [NEW] tags.
h. DO NOT add any information to "Assessed Current Situations" unless explicitly mentioned in reviews.

2. Content Enhancement and Information Preservation
For each subplan:
a. Improve clarity, coherence, and professionalism of existing content.
b. Fix grammar and spelling mistakes.
c. Expand concise sentences into more detailed, professional descriptions. For example, instead of "She is prone to constipation," write "The resident experiences a tendency towards constipation, which requires ongoing monitoring and management as part of her care plan."
d. Ensure all expansions remain factual and based solely on the information provided in the original content.
e. Preserve ALL information, including past reviews, treatments, and assessments.
f. In the Care Needs section, include a subsection titled "Comprehensive Medical Background" to capture all historical and background information.

### 3. Standardization and Proofreading
a. Ensure consistent formatting and language across all subplans.
b. Verify that all subplans follow the same structure and section headings.
c. Use consistent terminology for similar concepts across subplans.
d. Proofread the entire document for grammatical errors, paying special attention to:
   - Verb tense consistency
   - Subject-verb agreement
   - Proper use of articles (a, an, the)
   - Correct use of prepositions
   - Consistent capitalization of proper nouns and at the beginning of sentences
   - Correct and consistent punctuation, including commas, periods, and semicolons
e. Ensure all sentences are complete and make sense.

### 4. Review Chronology Correction
a. Collect all reviews from each subplan.
b. Sort the reviews in reverse chronological order, with the most recent review at the top and the oldest review at the bottom.
c. If multiple reviews exist for the same date, maintain their original order within that date.

5. Final Output Generation
Generate the following sections for each subplan:
a. Enhanced Care Plan:
Subplan [X]: [Subplan Title]

Assessed Current Situations:
• [Point 1]
• [Point 2]
• ...
[If empty, state: "This section was empty in the original and remains empty."]
Care Needs:
• [Point 1]
• [Point 2]
• ...
Comprehensive Medical Background:
• [Background point 1]
• [Background point 2]
• ...
[If empty, state: "This section was empty in the original and remains empty."]
Outcomes and Goals:
• [Point 1]
• [Point 2]
• ...
[If empty, state: "This section was empty in the original and remains empty."]
Description of Care Actions:
• [Point 1]
• [Point 2]
• ...
[If empty, state: "This section was empty in the original and remains empty."]
Reviews: [Enhanced content in reverse chronological order, most recent at the top]

Most Recent Review(s):

Date: [Date of most recent review(s)]
Content: [Content of most recent review(s)]

Reasoning: [Explain why these are the most recent reviews. Describe in detail how you integrated the review information into the care plan sections, including why certain sections were chosen for the new information. If no changes were made, explain why. Address how duplicate reviews, if any, were handled.]
b. Information Preservation Check:

Confirmation of adherence to critical instructions
Explicit statement that no information was moved between subplans or sections
Confirmation that all reviews from the most recent date were included
Verification that all information was preserved and expanded upon without fabrication

c. Quality Assurance Check:

Clarity and coherence assessment
Completeness of care needs and actions
Logical flow within sections
Consistency of terminology and phrasing
Adherence to original structure and content placement
Grammatical accuracy and clarity of expression
Confirmation of review chronology (most recent at the top)
Verification of consistent capitalization and punctuation
Confirmation that concise sentences have been professionally expanded
Areas requiring further clarification or expansion

Output:
Follow the structure outlined in section 5 (Final Output Generation) above for each subplan, ensuring all components are included in your response.
"""



# CARE_PLAN_TEMPLATE = """
# # Comprehensive Multi-Subplan Care Plan Update and Enhancement V4

# You are an AI assistant specializing in elder care plan documentation. Your task is to update, enhance, and standardize multiple care plan subplans in a single, comprehensive process. Follow these instructions meticulously to ensure the highest quality outcome.

# ## CRITICAL INSTRUCTIONS (Apply at all times):
# - NEVER omit any information from the original subplans, even if it seems redundant or outdated.
# - Maintain the exact original structure of each subplan.
# - If a section was empty in the original subplan, it MUST remain empty.
# - Always use the provided current date to identify the most recent reviews.
# - Include ALL reviews from the most recent date, even if they appear to be duplicates.
# - Format the Assessed Current Situations, Care Needs, Outcomes and Goals, and Description of Care Actions sections in a point-by-point format.
# - Ensure impeccable grammar, spelling, and clarity throughout the document.
# - Present all reviews in reverse chronological order, with the most recent at the top.
# - Maintain consistent capitalization and punctuation throughout the document.
# - Expand concise sentences into more detailed, professional descriptions without adding any new information.
# - Use "Comprehensive Medical Background" instead of "Historical Information".
# - Never add or fabricate information not present in the original content.
# - Output the final result in the specified JSON format.

# ## Input:
# - Subplans: {subplans}
# - Current Date: {current_date}

# ## Process Overview:
# 1. Review Identification and Update
# 2. Content Enhancement and Information Preservation
# 3. Standardization and Proofreading
# 4. Review Chronology Correction
# 5. Final Output Generation in JSON Format


# ## Detailed Instructions:


# ### 1. Review Identification and Update
# For each subplan:
# a. Identify the most recent review(s) by comparing dates to the provided current date: {current_date}.
# b. Use this method to compare dates:
#    - Compare years first (e.g., 24 for 2024)
#    - If years are the same, compare months (01-12)
#    - If months are the same, compare days (01-31)
# c. Select ALL reviews with the latest date, even if there are multiple entries for the same date.
# d. If multiple reviews exist for the most recent date, include ALL of them in your update.
# e. Update the care plan with new information from the most recent review(s).
# f. Integrate new information into appropriate sections (Care Needs, Outcome/Goal, Description of Care Actions).
# g. Mark new additions with [NEW] tags.
# h. DO NOT add any information to "Assessed Current Situations" unless explicitly mentioned in reviews.

# 2. Content Enhancement and Information Preservation
# For each subplan:
# a. Improve clarity, coherence, and professionalism of existing content.
# b. Fix grammar and spelling mistakes.
# c. Expand concise sentences into more detailed, professional descriptions. For example, instead of "She is prone to constipation," write "The resident experiences a tendency towards constipation, which requires ongoing monitoring and management as part of her care plan."
# d. Ensure all expansions remain factual and based solely on the information provided in the original content.
# e. Preserve ALL information, including past reviews, treatments, and assessments.
# f. In the Care Needs section, include a subsection titled "Comprehensive Medical Background" to capture all historical and background information.

# ### 3. Standardization and Proofreading
# a. Ensure consistent formatting and language across all subplans.
# b. Verify that all subplans follow the same structure and section headings.
# c. Use consistent terminology for similar concepts across subplans.
# d. Proofread the entire document for grammatical errors, paying special attention to:
#    - Verb tense consistency
#    - Subject-verb agreement
#    - Proper use of articles (a, an, the)
#    - Correct use of prepositions
#    - Consistent capitalization of proper nouns and at the beginning of sentences
#    - Correct and consistent punctuation, including commas, periods, and semicolons
# e. Ensure all sentences are complete and make sense.

# ### 4. Review Chronology Correction
# a. Collect all reviews from each subplan.
# b. Sort the reviews in reverse chronological order, with the most recent review at the top and the oldest review at the bottom.
# c. If multiple reviews exist for the same date, maintain their original order within that date.

# ### 5. Final Output Generation in JSON Format
# Generate the following JSON structure for each subplan:

# ```json
# {{
#   "FinalOutputGeneration": {{
#     "Subplans": [
#       {{
#         "SubplanTitle": "Subplan Title",
#         "EnhancedCarePlan": {{
#           "AssessedCurrentSituations": [
#             "Point 1",
#             "Point 2"
#           ],
#           "CareNeeds": [
#             "Point 1",
#             "Point 2"
#           ],
#           "ComprehensiveMedicalBackground": [
#             "Background point 1",
#             "Background point 2"
#           ],
#           "OutcomesAndGoals": [
#             "Point 1",
#             "Point 2"
#           ],
#           "DescriptionOfCareActions": [
#             "Point 1",
#             "Point 2"
#           ],
#           "Reviews": [
#             {{
#               "Date": "Date of review",
#               "Content": "Content of review"
#             }}
#           ]
#         }},
#         "MostRecentReview": {{
#           "Date": "Date of most recent review",
#           "Content": "Content of most recent review",
#           "Reasoning": "Explanation of integration and changes"
#         }}
#       }}
#     ],
#     "InformationPreservationCheck": {{
#       "AdherenceToCriticalInstructions": "",
#       "NoInformationMovedBetweenSubplansOrSections": "",
#       "AllRecentReviewsIncluded": "",
#       "InformationPreservation": ""
#     }},
#     "QualityAssuranceCheck": {{
#       "ClarityAndCoherenceAssessment": "",
#       "CompletenessOfCareNeedsAndActions": "",
#       "LogicalFlowWithinSections": "",
#       "ConsistencyOfTerminologyAndPhrasing": "",
#       "AdherenceToOriginalStructureAndContentPlacement": "",
#       "GrammaticalAccuracyAndClarity": "",
#       "ReviewChronology": "",
#       "ConsistentCapitalizationAndPunctuation": "",
#       "ProfessionalExpansionOfConciseSentences": "",
#       "AreasRequiringFurtherClarificationOrExpansion": ""
#     }}
#   }}
# }}

# Ensure that all information from the original subplans is included in the appropriate sections of this JSON structure. Pay particular attention to including all historical information, reviews, and medical background data.

# ## Output:
# Provide the complete JSON structure as outlined above, ensuring all components are included and all original information is preserved.


# """
# Comprehensive Multi-Subplan Care Plan Update and Enhancement V6

CARE_PLAN_TEMPLATE = """

You are an AI assistant specializing in care plan documentation. Your task is to update, enhance, and standardize multiple care plan subplans in a single, comprehensive process. Follow these instructions meticulously to ensure the highest quality outcome.

## CRITICAL INSTRUCTIONS (Apply at all times):
- NEVER omit any information from the original subplans, even if it seems redundant or outdated.
- Preserve ALL information, including past reviews, assessments, and events, regardless of where they appear in the original text.
- Maintain the exact original structure of each subplan, including all original section headings.
- If a section was empty in the original subplan, it MUST remain empty.
- Always use the provided current date to identify the most recent reviews.
- Include ALL reviews from the most recent date, even if they appear to be duplicates.
- Format all sections in a point-by-point format for clarity.
- Ensure impeccable grammar, spelling, and clarity throughout the document.
- Present all reviews in reverse chronological order, with the most recent at the top.
- Maintain consistent capitalization and punctuation throughout the document.
- Expand concise sentences into more detailed, professional descriptions without adding any new information.
- Never add or fabricate information not present in the original content.
- Output the final result in the specified JSON format.

## Input:
- Subplans: {subplans}
- Current Date: {current_date}
- Combination Instructions: {combine_instructions}

## Process Overview:
1. Review Identification and Update
2. Content Enhancement and Information Preservation
3. Standardization and Proofreading
4. Review Chronology Correction
5. Subplan Combination Analysis
6. Final Output Generation in JSON Format

## Detailed Instructions:

### 1. Review Identification and Update
For each subplan:
a. Identify the most recent review(s) by comparing dates to the provided current date: {current_date}.
b. Use this method to compare dates:
   - Compare years first (e.g., 24 for 2024)
   - If years are the same, compare months (01-12)
   - If months are the same, compare days (01-31)
c. Select ALL reviews with the latest date, even if there are multiple entries for the same date.
d. If multiple reviews exist for the most recent date, include ALL of them in your update.
e. Update the care plan with new information from the most recent review(s).
f. Integrate new information into appropriate sections of the original subplan structure.
g. DO NOT add any information to sections unless explicitly mentioned in reviews or original content.

### 2. Content Enhancement and Information Preservation
For each subplan:
a. Improve clarity, coherence, and professionalism of existing content.
b. Fix grammar and spelling mistakes.
c. Expand concise sentences into more detailed, professional descriptions.
d. Ensure all expansions remain factual and based solely on the information provided in the original content.
e. Preserve ALL information, including past reviews, assessments, and events, regardless of where they appear in the original text.
f. Create a new section titled "Additional Information" to capture any information that doesn't fit into the existing sections.

### 3. Standardization and Proofreading
a. Ensure consistent formatting and language across all subplans.
b. Verify that all subplans follow their original structure and section headings.
c. Use consistent terminology for similar concepts across subplans.
d. Proofread the entire document for grammatical errors, paying special attention to:
   - Verb tense consistency
   - Subject-verb agreement
   - Proper use of articles (a, an, the)
   - Correct use of prepositions
   - Consistent capitalization of proper nouns and at the beginning of sentences
   - Correct and consistent punctuation, including commas, periods, and semicolons
e. Ensure all sentences are complete and make sense.

### 4. Review Chronology Correction
a. Collect all reviews from each subplan.
b. Sort the reviews in reverse chronological order, with the most recent review at the top and the oldest review at the bottom.
c. If multiple reviews exist for the same date, maintain their original order within that date.

### 5. Subplan Combination Analysis
a. Review the provided combination instructions: {combine_instructions}
b. Analyze all subplans for similarities based on the combination instructions.
c. If subplans meet the criteria for combination as per the instructions, proceed with combining them.
d. When combining subplans:
   - Merge similar sections while preserving all unique information.
   - Use clear headings to distinguish information from different original subplans.
   - Ensure no information is lost or duplicated in the process.
e. If subplans do not meet the combination criteria, keep them separate.
f. Provide a clear explanation of the combination decision in the "Reasoning" section of the output.

### 6. Final Output Generation in JSON Format
Generate the following JSON structure for each resulting subplan (original or combined):

```json
{{
  "FinalOutputGeneration": {{
    "Subplans": [
      {{
        "SubplanTitle": "Original Subplan Title" or "Combined Subplan: [Titles of Original Subplans]",
        "EnhancedCarePlan": {{
          "AssessedCurrentSituations": [
            "Point 1",
            "Point 2",
            // ... additional points or "This section was empty in the original and remains empty."
          ],
          "CareNeeds": [
            "Point 1",
            "Point 2"
            // ... additional points or "This section was empty in the original and remains empty."
          ],
          "OutcomesAndGoals": [
            "Point 1",
            "Point 2"
            // ... additional points or "This section was empty in the original and remains empty."
          ],
          "DescriptionOfCareActions": [
            "Point 1",
            "Point 2"
            // ... additional points or "This section was empty in the original and remains empty."
          ],
          "AdditionalInformation": [
            "Additional point 1",
            "Additional point 2"
          ],
          "Reviews": [
            {{
              "Date": "Date of review",
              "Name":"Name of the reviewer"
              "Content": "Content of review"
            }}
          ]
        }},
        "MostRecentReview": {{
          "Date": "Date of most recent review",
          "Content": "Content of most recent review",
          "Reasoning": "Explanation of integration, changes, and combination decisions"
        }}
      }}
    ],
    
  }}
}}

Ensure that all information from the original subplans is included in the appropriate sections of this JSON structure, whether in original or combined form. Pay particular attention to including all historical information, reviews, and events, regardless of where they appear in the original text.

Output:
Provide the complete JSON structure as outlined above, ensuring all components are included and all original information is preserved. Include a clear explanation of any combination decisions made based on the provided instructions.

"""

# "InformationPreservationCheck": {{
#       "AdherenceToCriticalInstructions": "",
#       "NoInformationMovedBetweenSubplansOrSections": "",
#       "AllRecentReviewsIncluded": "",
#       "InformationPreservation": "",
#       "CombinationDecisionExplanation": ""
#     }},
#     "QualityAssuranceCheck": {{
#       "ClarityAndCoherenceAssessment": "",
#       "CompletenessOfInformation": "",
#       "LogicalFlowWithinSections": "",
#       "ConsistencyOfTerminologyAndPhrasing": "",
#       "AdherenceToOriginalStructureAndContentPlacement": "",
#       "GrammaticalAccuracyAndClarity": "",
#       "ReviewChronology": "",
#       "ConsistentCapitalizationAndPunctuation": "",
#       "ProfessionalExpansionOfConciseSentences": "",
#       "AreasRequiringFurtherClarificationOrExpansion": ""
#     }}

import json
from typing import Dict, Any, List
from datetime import date
import time
import re

def extract_json(text):
    """Attempt to extract JSON from the given text."""
    json_match = re.search(r'(\{.*\})', text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    return None

def display_care_plan(json_output: str) -> None:
    """
    Display the care plan JSON output in a readable format.
    
    :param json_output: JSON string containing the care plan data
    """
    try:
        data = json.loads(json_output)
        final_output = data.get("FinalOutputGeneration", {})
        subplans = final_output.get("Subplans", [])
        
        for i, subplan in enumerate(subplans):
            print(f"\n\n\n\n{'='*150}")
            print(f"Subplan {i}: {subplan['SubplanTitle']}")
            print(f"{'='*150}")
            
            enhanced_plan = subplan.get("EnhancedCarePlan", {})
            
            sections = [
                ("Assessed Current Situations", "AssessedCurrentSituations"),
                ("Care Needs", "CareNeeds"),
                ("Outcomes and Goals", "OutcomesAndGoals"),
                ("Description of Care Actions", "DescriptionOfCareActions"),
                ("Additional Information", "AdditionalInformation")
            ]
            
            for section_title, section_key in sections:
                print(f"\n{section_title}:")
                print("-" * len(section_title))
                for item in enhanced_plan.get(section_key, []):
                    print(f"- {item}")
            
            print("\nReviews:")
            print("-" * 7)
            for review in enhanced_plan.get("Reviews", []):
                print(f"Date: {review['Date']}")
                print(f"Name: {review['Name']}")
                print(f"Content: {review['Content']}")
                print()
            
            most_recent = subplan.get("MostRecentReview", {})
            print("\nMost Recent Review:")
            print("-" * 20)
            print(f"Date: {most_recent.get('Date', 'N/A')}")
            print(f"Content: {most_recent.get('Content', 'N/A')}")
            print(f"\nReasoning: {most_recent.get('Reasoning', 'N/A')}")
    
    except json.JSONDecodeError:
        print("Error: Invalid JSON input")
    except KeyError as e:
        print(f"Error: Missing key in JSON structure: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def process_care_plans(subplans: List[str], combine_instructions: str, max_retries: int = 3) -> Dict:
    """
    Processes the care plans using the Gemini LLM.
    
    Args:
    - subplans (List[str]): List of subplans to process.
    - combine_instructions (str): Instructions for combining subplans.
    - max_retries (int): Maximum number of retry attempts.
    
    Returns:
    - Dict: Processed and parsed care plan data.
    """
    gemini = GeminiInitializer()
    today = date.today()
    formatted_date = today.strftime("%d/%m/%y") # "17/07/2024"  # today.strftime("%d/%m/%y")
    print(formatted_date)
    formatted_subplans = "\n\n".join(f"Subplan {i+1}:\n{subplan}" for i, subplan in enumerate(subplans))
    prompt = CARE_PLAN_TEMPLATE.format(subplans=formatted_subplans, combine_instructions=combine_instructions, current_date=formatted_date)
    print(prompt)
    for attempt in range(max_retries):
        try:
            response = gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
            
            # Attempt to extract JSON from the response
            json_str = extract_json(response)
            if json_str is None:
                raise ValueError("No JSON found in the response")
            
            # Attempt to parse the JSON
            parsed_json = json.loads(json_str)
            
            # If successful, display the care plan and return the parsed JSON
            display_care_plan(json_str)
            return parsed_json
        
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                print("Max retries reached. Unable to process care plans.")
                return None
            print("Retrying...")
    
    return None

def pipeline(subplans: List[str], combine_instructions: str) -> Dict:
    """
    Main pipeline function to process care plans.
    
    Args:
    - subplans (List[str]): List of subplans to process.
    - combine_instructions (str): Instructions for combining subplans.
    
    Returns:
    - Dict: Processed and parsed care plan data.
    """
    start_time = time.time()
    
    result = process_care_plans(subplans, combine_instructions)
    
    end_time = time.time()
    inference_time = end_time - start_time
    print(f"Inference Time: {inference_time} seconds")
    
    if result is None:
        print("Failed to process care plans.")
    
    return result

# Example usage
if __name__ == "__main__":
    from sub_plan import sub_plan_1, sub_plan_2, sub_plan_3, sub_plan_4, sub_plan_5, sub_plan_6, sub_plan_7, sub_plan_8, combine_instructions
    
   #  sub_plan_list = [sub_plan_1, sub_plan_2, sub_plan_3, sub_plan_4, sub_plan_5, sub_plan_6, sub_plan_7, sub_plan_8]
    sub_plan_list = [sub_plan_4, sub_plan_5]
    
    result = pipeline(sub_plan_list, combine_instructions)