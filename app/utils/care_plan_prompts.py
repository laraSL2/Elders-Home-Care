# Care Plan Generation Template
CARE_PLAN_TEMPLATE2 = """

You are an AI assistant specializing in care plan documentation. Your task is to update, enhance, and standardize multiple care plan subplans in a single, comprehensive process. Follow these instructions meticulously to ensure the highest quality outcome.

## CRITICAL INSTRUCTIONS (Apply at all times):
- NEVER omit any information from the original subplans, even if it seems redundant or outdated.
- Preserve ALL information, including past reviews, assessments, and events, regardless of where they appear in the original text.
- Maintain the exact original structure of each subplan, including all original section headings.
- If a section was empty in the original subplan, it MUST remain empty.
- Always use the provided current date to identify the most recent reviews.
- Include ALL reviews from the most recent date, even if they appear to be duplicates.
- IMPORTANT: Only update review content within these suitable sections:
          * Assessed current situations
          * Care needs
          * Outcome/goal
          * Description of care actions
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
6. Proofread and Polish the Final Document
7. Final Output Generation in JSON Format

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
e. Update the subplan with new information from the most recent review(s).
f. Integrate new information ONLY into these appropriate sections of the original subplan structure:
   - Assessed current situations
   - Care needs
   - Outcome/goal
   - Description of care actions
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

###6. Proofread and Polish the Final Document

 a) Grammar Check:
    - Review the entire document for grammatical errors
    - Pay special attention to:
      - Subject-verb agreement
      - Proper use of tenses
      - Correct pronoun usage
      - Appropriate punctuation

  b) Spelling Review:
    - Carefully check for spelling mistakes throughout the text
    - Look out for:
        - Commonly misspelled words
        - Proper nouns and technical terms
        - Homophones (e.g., their/there/they're, its/it's)

  c) Sentence Formation and Improvement:
    - Evaluate each sentence for clarity and effectiveness
    - If a sentence is unclear or poorly constructed:
       - Identify the main idea and supporting details
       - Rewrite the sentence to express the idea more clearly
       - Consider breaking long, complex sentences into shorter ones
    - Ensure variety in sentence structure to maintain reader interest
    - Use active voice where appropriate to strengthen writing
    - Eliminate unnecessary words or phrases to improve concision

  d) Consistency:
   - Ensure consistent formatting throughout the document
   - Check for uniform capitalization in headings and titles
   - Verify consistent use of terminology

  e) Readability:
    - Review overall structure for clarity and flow
    - Ensure smooth transitions between paragraphs and sections
    - Use transitional phrases to connect ideas effectively

  f) Final Pass:
    - Read the document aloud to catch any remaining errors
    - Consider using grammar and spell-checking tools to supplement manual review
    - If possible, have another person review the document for a fresh perspective

### 7. Final Output Generation in JSON Format
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


CARE_PLAN_TEMPLATE = """
You are an AI assistant specializing in care plan documentation. Your task is to update, enhance, and standardize multiple care plan subplans in a single, comprehensive process. Follow these instructions meticulously to ensure the highest quality outcome.

## CRITICAL INSTRUCTIONS (Apply at all times):
- NEVER omit any information from the original subplans, even if it seems redundant or outdated.
- Preserve ALL information, including past reviews, assessments, and events, regardless of where they appear in the original text.
- Maintain the exact original structure of each subplan, including all original section headings.
- If a section was empty in the original subplan, it MUST remain empty.
- Always use the provided current date to identify the most recent reviews.
- Include ALL reviews from the most recent date, even if they appear to be duplicates.
- IMPORTANT: Only update review content within these suitable sections:
          * Assessed current situations
          * Care needs
          * Outcome/goal
          * Description of care actions
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
6. Proofread and Polish the Final Document
7. Final Output Generation in JSON Format

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
e. Update the subplan with new information from the most recent review(s).
f. Integrate new information ONLY into these appropriate sections of the original subplan structure:
   - Assessed current situations
   - Care needs
   - Outcome/goal
   - Description of care actions
g. DO NOT add any information to sections unless explicitly mentioned in reviews or original content.

Example:
  Original subplan X:
  Assessed current situations:
  - Patient has difficulty walking
  Care needs:
  - Assistance with mobility

  Review (date: 15/06/2024):
  "Patient now using a walker. Needs supervision during transfers."

  Updated subplan:
  Assessed current situations:
  - Patient has difficulty walking
  - Patient is now using a walker for mobility assistance
  Care needs:
  - Assistance with mobility
  - Supervision during transfers

### 2. Content Enhancement and Information Preservation
For each subplan:
a. Improve clarity, coherence, and professionalism of existing content.
b. Fix grammar and spelling mistakes.
c. Expand concise sentences into more detailed, professional descriptions.
d. Ensure all expansions remain factual and based solely on the information provided in the original content.
e. Preserve ALL information, including past reviews, assessments, and events, regardless of where they appear in the original text.
f. Create a new section titled "Additional Information" to capture any information that doesn't fit into the existing sections.

Example-1:
  Original: "pt needs help w/ meds"
  Enhanced: "The patient requires assistance with medication administration. Staff should ensure that all prescribed medications are administered correctly and at the appropriate times."

Example-2:
  Original text:
  "resident forgets to eat meals frequently"

  Enhanced text:
  "The resident frequently forgets to attend scheduled mealtimes. This memory lapse affects their nutritional intake and overall health. Staff should implement reminders and assistance to ensure the resident participates in regular meals."

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

Example:
  Original text:
  "patient need help with adl's. cant dress self"

  Standardized and proofread text:
  "The patient requires assistance with Activities of Daily Living (ADLs). Specifically, they are unable to dress themselves independently."

### 4. Review Chronology Correction
a. Collect all reviews from each subplan.
b. Sort the reviews in reverse chronological order, with the most recent review at the top and the oldest review at the bottom.
c. If multiple reviews exist for the same date, maintain their original order within that date.

Example:
Original order:
1. Review dated 10/04/2023
2. Review dated 25/06/2024
3. Review dated 05/05/2024

Corrected order:
1. Review dated 25/06/2024
2. Review dated 05/05/2024
3. Review dated 10/04/2023

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

Example:
Combination instruction: "Combine subplans if they address related aspects of the resident's care."

Subplan 1: Medication Management
Subplan 2: Pain Management

Combined Subplan: "Medication and Pain Management"
Reasoning: "These subplans were combined as they both relate to the resident's medication needs, with pain management being a key aspect of their overall medication regimen."

### 6. Proofread and Polish the Final Document

a) Grammar Check:
   - Review the entire document for grammatical errors
   - Pay special attention to:
     - Subject-verb agreement
     - Proper use of tenses
     - Correct pronoun usage
     - Appropriate punctuation

Example:
Original: "The patients needs is not being met"
Corrected: "The patient's needs are not being met."

b) Spelling Review:
   - Carefully check for spelling mistakes throughout the text
   - Look out for:
       - Commonly misspelled words
       - Proper nouns and technical terms
       - Homophones (e.g., their/there/they're, its/it's)

Example:
Original: "The resident recieved there medication"
Corrected: "The resident received their medication."

c) Sentence Formation and Improvement:
   - Evaluate each sentence for clarity and effectiveness
   - If a sentence is unclear or poorly constructed:
      - Identify the main idea and supporting details
      - Rewrite the sentence to express the idea more clearly
      - Consider breaking long, complex sentences into shorter ones
   - Ensure variety in sentence structure to maintain reader interest
   - Use active voice where appropriate to strengthen writing
   - Eliminate unnecessary words or phrases to improve concision

Example:
Original: "It was observed that the patient was experiencing pain and discomfort in their lower back region which was causing them to have difficulty with mobility and performing daily activities."
Improved: "The patient reported lower back pain, which impaired their mobility and ability to perform daily activities."

d) Consistency:
  - Ensure consistent formatting throughout the document
  - Check for uniform capitalization in headings and titles
  - Verify consistent use of terminology

Example:
Original: "The PATIENT needs assistance with ADLs... The resident requires help with activities of daily living."
Consistent: "The patient needs assistance with Activities of Daily Living (ADLs)... The patient requires help with ADLs."

e) Readability:
   - Review overall structure for clarity and flow
   - Ensure smooth transitions between paragraphs and sections
   - Use transitional phrases to connect ideas effectively

Example:
Original:
"The patient has difficulty walking. They use a walker. They need help with bathing."

Improved:
"The patient experiences mobility challenges and relies on a walker for ambulation. Due to these limitations, they also require assistance with bathing activities."

f) Final Pass:
   - Read the document aloud to catch any remaining errors
   - Consider using grammar and spell-checking tools to supplement manual review
   - If possible, have another person review the document for a fresh perspective

### 7. Final Output Generation in JSON Format
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

FB_REFINING_TEMPLATE = """
You are an expert in analyzing and refining care plan information for patients. Your task is to carefully review the provided care plan data, incorporate expert feedback, and produce an updated, well-structured care plan.

SUB_PLAN:
{input_data}

EXPERT FEEDBACK:
{expert_feedback}

INSTRUCTIONS:
1. Thoroughly analyze the input data and expert feedback.
2. Identify all relevant information related to the patient's care plan.
3. Incorporate changes based on the expert feedback, ensuring you only use information present in the input data or feedback.
4. Maintain the original structure and formatting where appropriate.
5. Do not introduce new information or make assumptions beyond what is provided.
6. Ensure all medical terminology and abbreviations are interpreted accurately and consistently.
7. Be mindful of patient privacy and confidentiality standards.
8. If combining multiple subplans, integrate the information logically and note this in the reasoning.
9. For any empty sections in the original plan, indicate that they remain empty in the output.

Based on your analysis and the above instructions, please provide the refined care plan in the following format:

{{
  "SubplanTitle": "Original Subplan Title" or "Combined Subplan: [Titles of Original Subplans]",
  "RefinedCarePlan": {{
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
    "Reviews": [
      {{
        "Date": "Date of review",
        "Name": "Name of the reviewer",
        "Content": "Content of review"
      }}
      // ... additional reviews
    ]
  }},
  "Reasoning": "Explanation of integration, changes, and combination decisions"
}}

Ensure that all sections are filled out according to the available information. If a section is empty in the original and remains empty, explicitly state this. Provide a clear reasoning for any changes, integrations, or combinations made in the Reasoning section.
"""

