from gemini_initializer import GeminiInitializer
from datetime import date
from typing import List, Dict
import json
import sub_plan

import time


CARE_PLAN_TEMPLATE2 = """
You are an expert in elder care plan documentation. Your task is to analyze, compare, and enhance the quality of N given subplans. Based on the comparison, decide whether to combine highly similar subplans or maintain them as separate subplans. You can combine any number of similar subplans, not just pairs. Provide a clear and detailed explanation of your reasoning and changes made. Follow these steps:

Instructions:
Task-01: Comprehensive Analysis and Similarity Assessment
   1. Input Analysis:
      - Thoroughly analyze each of the given subplans.
      - Identify the main components for each subplan: Assessed Current Situation, Care Needs, Outcomes and Goals, Description of Care Actions, and Reviews.

   2. Similarity Comparison:
      - Compare each subplan with every other subplan for similarities in all components.
      - Identify groups of subplans with high similarity across multiple components.
      - Consider the overall context and purpose of each subplan, not just textual similarity.

   3. Decision Making:
      - Identify groups of subplans that are highly similar and would benefit from combination.
      - There is no fixed similarity percentage - use your expert judgment to determine which subplans should be combined based on their content and purpose.
      - Subplans can be combined in groups of two, three, or more if appropriate.
      - Maintain unique subplans as separate.

   4. Combination Process:
      - For each group of subplans to be combined:
        a. Create a new, comprehensive subplan that incorporates all unique elements from the original subplans.
        
        b. Merge the Assessed Current Situation sections, removing redundancies and preserving unique information.
        c. Combine Care Needs, eliminating duplicates and ensuring all unique needs are represented.
        d. Merge Outcomes and Goals, ensuring all unique goals are included.
        e. Combine Description of Care Actions, removing redundancies and preserving all unique actions.
        f. Merge Reviews chronologically, removing duplicate entries if they exist.

Task-02: Enhancement
   For each resulting subplan (combined or individual):
   1. Improve clarity and coherence of the content.
   2. Ensure consistent and professional language throughout.
   3. Fix any grammar and spelling mistakes.
   4. Enhance content accuracy and completeness:
      - Ensure logical consistency and chronological order of events.
      - Infer and include implied information based on context.
      - Remove redundancies while preserving all relevant details.
   5. Reformat and expand sentences for better readability and comprehensiveness.

Input:
{Subplans}

Your goal is to analyze, potentially combine, and enhance the quality and usability of the care plan(s) while maintaining all relevant and current information.

OUTPUT_FORMAT:

Similarity Analysis Summary:
[Provide a detailed summary of the similarity analysis, explaining which subplans were found to be highly similar and will be combined. Explain your reasoning for each combination.]

Enhanced Care Plans:

[For each resulting subplan (whether original or combined), use the following format:]

Subplan [X] (Original) or Combined Subplan [Y] (from original subplans [A], [B], [C], ...):
   Title: [Provide a concise title for the subplan]

   Assessed Current Situation:
      [Enhanced assessment of the current situation]

   Care Needs:
      [Enhanced care needs]

   Outcomes and Goals:
      [Enhanced goals and outcomes]

   Description of Care Actions:
      [Enhanced care actions]
            
   Reviews:
      [Combined reviews, organized in chronological order from most recent to oldest. Do not use review content to update the plan.]

Reasoning and Changes:
   - Decisions: [Explain which subplans were combined, if any, and which remained separate]
   - Reasoning: [Provide detailed reasoning for the decisions made, including why certain subplans were combined and others were kept separate]
   - General Changes: [Describe overall enhancements made across all subplans]
   - Specific Changes: [List specific significant changes made to each subplan or group of combined subplans]

IMPORTANT: The content in the Reviews section is for reference only and should not be used to directly modify the care plan. Any changes to the care plan based on reviews should be made through a formal update process.

FINAL_PLAN_SUMMARY:
[Provide a comprehensive summary of the final result, including:
 - The number of original subplans (N)
 - The number of resulting subplans after analysis and combination (M)
 - A brief overview of how the subplans were reorganized (e.g., "3 groups of subplans were combined, resulting in 12 final subplans from the original 15")
 - Any key observations or recommendations based on the analysis]
"""

CARE_PLAN_TEMPLATE3 = """

You are an expert in elder care plan documentation. Your task is to analyze, compare, and enhance the quality of the provided subplans. Based on the comparison and given instructions, you'll decide whether to combine similar subplans or maintain them separately. Follow these steps:

## Task 1: Comprehensive Analysis and Similarity Assessment

1. Input Analysis:
   - Thoroughly analyze each of the given subplans.
   - Identify and preserve the exact structure of each subplan, including: Assessed Current Situation, Care Needs, Outcomes and Goals, Description of Care Actions, and Reviews.

2. Similarity Comparison:
   - Compare each subplan with every other subplan for similarities in all components.
   - Use the provided information in {combine_instructions} to guide your decision on which subsections can be combined.
   - Identify groups of subplans with high similarity across multiple components.
   - Consider the overall context and purpose of each subplan, not just textual similarity.

3. Decision Making:
   - Identify groups of subplans that are highly similar and would benefit from combination.
   - Use your expert judgment to determine which subplans should be combined based on their content and purpose.
   - Subplans can be combined in groups of two, three, or more if appropriate.
   - Maintain unique subplans as separate.

4. Combination Process:
   For each group of subplans to be combined:
   a. Create a new, comprehensive subplan that incorporates all unique elements from the original subplans.
   b. Maintain the original structure of the subplans (Assessed Current Situation, Care Needs, Outcomes and Goals, Description of Care Actions, and Reviews).
   c. Ensure that information from each section is merged into the corresponding section of the combined subplan.
   d. Avoid moving information between sections (e.g., from Care Needs to Assessed Current Situation) unless it's clearly misplaced in the original.
   e. Preserve all unique information from each original subplan, even if it seems redundant.

## Task 2: Enhancement

For each resulting subplan (combined or individual):
1. Improve clarity and coherence of the content within each section.
2. Ensure consistent and professional language throughout.
3. Fix any grammar and spelling mistakes.
4. Enhance content accuracy and completeness:
   - Ensure logical consistency and chronological order of events.
   - Infer and include implied information based on context, but clearly mark any inferred information with [Inferred: ].
   - Remove exact duplicates of information, but preserve similar information that may provide additional context.
5. Reformat and expand sentences for better readability and comprehensiveness, while maintaining the original meaning and intent.

## Input:
Subplans: {subplans}
Combination Instructions: {combine_instructions}

## Output Format:

### Similarity Analysis Summary:
[Provide a detailed summary of the similarity analysis, explaining which subplans were found to be highly similar and will be combined. Explain your reasoning for each combination.]

### Enhanced Care Plans:

[For each resulting subplan (whether original or combined), use the following format:]

Subplan [X] (Original) or Combined Subplan [Y] (from original subplans [A], [B], [C], ...):
   Title: [Provide a concise title for the subplan]

   Assessed Current Situation:
      [Enhanced assessment of the current situation, preserving all original information]

   Care Needs:
      [Enhanced care needs, preserving all original information]

   Outcomes and Goals:
      [Enhanced goals and outcomes, preserving all original information]

   Description of Care Actions:
      [Enhanced care actions, preserving all original information]
            
   Reviews:
      [Combined reviews, organized in chronological order from most recent to oldest. Do not use review content to update the plan.]

### Reasoning and Changes:
   - Decisions: [Explain which subplans were combined, if any, and which remained separate]
   - Reasoning: [Provide detailed reasoning for the decisions made, including why certain subplans were combined and others were kept separate]
   - General Changes: [Describe overall enhancements made across all subplans]
   - Specific Changes: [List specific significant changes made to each subplan or group of combined subplans, including any information that was inferred or clarified]

IMPORTANT: The content in the Reviews section is for reference only and should not be used to directly modify the care plan. Any changes to the care plan based on reviews should be made through a formal update process.

### Final Plan Summary:
[Provide a comprehensive summary of the final result, including:
 - The number of original subplans
 - The number of resulting subplans after analysis and combination
 - A brief overview of how the subplans were reorganized (e.g., "3 groups of subplans were combined, resulting in 12 final subplans from the original 15")
 - Any key observations or recommendations based on the analysis]

### Information Preservation Check:
[List any information from the original subplans that could not be incorporated into the enhanced care plans, explaining why it was omitted.]
"""


CARE_PLAN_TEMPLATE3 = """
# Expert Care Plan Documentation Analysis and Enhancement

As an expert in elder care plan documentation, your task is to enhance the quality of the provided subplans while strictly maintaining the original structure and content placement. Follow these steps meticulously:

## CRITICAL INSTRUCTIONS:
- DO NOT MOVE ANY EXISTING INFORMATION BETWEEN SECTIONS UNDER ANY CIRCUMSTANCES.
- DO NOT suggest moving information to other sections or plans.
- Each piece of existing information must remain exactly where it was in the original subplan.

## Task 1: Text Quality Enhancement and Expansion

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
   - Do not move any information between the following sections: Assessed Current Situation, Care Needs, Outcomes and Goals, Description of Care Actions.
   - If information seems misplaced, add a note in [brackets] suggesting where it might be more appropriate, but leave the information in its original location.

4. Review Section Handling:
   - Do not use information from the Reviews section to update or modify other sections.
   - Enhance the Reviews section independently, improving clarity and expanding on existing information without altering the original content or moving information to other sections.

5. Duplication Management:
   - Remove exact duplicates of information within the same section.
   - Preserve similar information that may provide additional context or nuance, even if it appears redundant.

6. Chronological Ordering:
   - Within each section, ensure events or information are presented in a logical, chronological order where applicable.

7. Final Check:
   - After all enhancements and expansions, review the subplan to ensure no information has been moved between sections.
   - Verify that all expansions and enhancements remain within their original sections.
   - Confirm that sections that were originally empty remain empty.

## Task 2: Comprehensive Analysis and Similarity Assessment

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
         [Enhanced assessment of the current situation, strictly preserving all original information and placement. If this section was empty in the original, it should remain empty.]

      Care Needs:
         [Enhanced care needs, strictly preserving all original information and placement. If this section was empty in the original, it should remain empty.]

      Outcomes and Goals:
         [Enhanced goals and outcomes, strictly preserving all original information and placement. If this section was empty in the original, it should remain empty.]

      Description of Care Actions:
         [Enhanced care actions, strictly preserving all original information and placement. If this section was empty in the original, it should remain empty.]

      Reviews:
         [Reviews organized in chronological order from most recent to oldest. Do not use review content to update other sections.]

   ### Similarity Analysis Summary:
   [Provide a detailed summary of the similarity analysis, explaining which subplans were found to be highly similar and whether they will be combined based on the {combine_instructions}. Explain your reasoning for each decision.]

   ### Reasoning and Changes:
      - Decisions: [Explain which subplans were combined, if any, and which remained separate]
      - Reasoning: [Provide detailed reasoning for the decisions made]
      - General Enhancements: [Describe overall enhancements made across all subplans, emphasizing that no information was moved between sections]
      - Specific Enhancements: [List specific significant enhancements made to each subplan, including any notes about potentially misplaced information]

   ### Final Plan Summary:
      [Provide a comprehensive summary of the final result, including:
    - The number of original subplans
    - The number of resulting subplans after analysis and potential combination
    - A brief overview of any reorganization (if applicable)
    - Any key observations or recommendations based on the analysis]

   ### Information Preservation Check:
      [Confirm that all original information has been preserved in its original sections. If any information seems misplaced, list it here along with a suggestion for where it might be more appropriate, but emphasize that it was not moved in the actual care plan. Confirm that sections that were originally empty have remained empty.]

   ### Quality Assurance Check:
      [Provide a brief assessment of the overall quality of the enhanced care plans, addressing:
    - Clarity and coherence of information
    - Completeness of care needs and actions
    - Logical flow within each section
    - Consistency of terminology and phrasing
    - Strict adherence to the original structure and content placement
    - Any areas that may require further clarification or expansion]
"""
CARE_PLAN_TEMPLATE = """
# Expert Care Plan Documentation Analysis and Enhancement

As an expert in elder care plan documentation, your task is to enhance the quality of the provided subplans while strictly maintaining the original structure and content placement. Follow these steps meticulously:

## CRITICAL INSTRUCTION:
- DO NOT MOVE ANY INFORMATION BETWEEN SECTIONS UNDER ANY CIRCUMSTANCES.
- Each piece of information must remain exactly where it was in the original subplan.
- If a section was empty in the original, it must remain empty in the enhanced version.
- Failure to follow this instruction could result in critical care information being misplaced or lost.

## Task 1: Text Quality Enhancement and Expansion

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
   - Do not move any information between the following sections: Assessed Current Situation, Care Needs, Outcomes and Goals, Description of Care Actions.
   - If information seems misplaced, add a note in [brackets] suggesting where it might be more appropriate, but leave the information in its original location.

4. Review Section Handling:
   - Do not use information from the Reviews section to update or modify other sections.
   - Enhance the Reviews section independently, improving clarity and expanding on existing information without altering the original content or moving information to other sections.

5. Duplication Management:
   - Remove exact duplicates of information within the same section.
   - Preserve similar information that may provide additional context or nuance, even if it appears redundant.

6. Chronological Ordering:
   - Within each section, ensure events or information are presented in a logical, chronological order where applicable.

7. Final Check:
   - After all enhancements and expansions, review the subplan to ensure no information has been moved between sections.
   - Verify that all expansions and enhancements remain within their original sections.
   - Confirm that sections that were originally empty remain empty.

## Task 2: Comprehensive Analysis and Similarity Assessment

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
- Subplans: {subplans}
- Combination Instructions: {combine_instructions}

## Output Format:

### Enhanced Care Plans:

[For each resulting subplan (whether original or combined), use the following format:]

Subplan [X] (Original) or Combined Subplan [Y] (from original subplans [A], [B], [C], ...):
- Title: [Provide a concise title for the subplan]

- Assessed Current Situation:
  - [Point 1 of enhanced assessment]
  - [Point 2 of enhanced assessment]
  - [...]
  [If this section was empty in the original, state: "This section was empty in the original and remains empty."]

- Care Needs:
  - [Point 1 of enhanced care needs]
  - [Point 2 of enhanced care needs]
  - [...]
  [If this section was empty in the original, state: "This section was empty in the original and remains empty."]

- Outcomes and Goals:
  - [Point 1 of enhanced goals and outcomes]
  - [Point 2 of enhanced goals and outcomes]
  - [...]
  [If this section was empty in the original, state: "This section was empty in the original and remains empty."]

- Description of Care Actions:
  - [Point 1 of enhanced care actions]
  - [Point 2 of enhanced care actions]
  - [...]
  [If this section was empty in the original, state: "This section was empty in the original and remains empty."]

- Reviews:
  - [Most recent review point]
  - [Second most recent review point]
  - [...]

### Similarity Analysis Summary:
- [Key point 1 about similarity analysis]
- [Key point 2 about similarity analysis]
- [...]

### Reasoning and Changes:
- Decisions:
  - [Decision point 1]
  - [Decision point 2]
  - [...]
- Reasoning:
  - [Reasoning point 1]
  - [Reasoning point 2]
  - [...]
- General Enhancements:
  - [Enhancement point 1]
  - [Enhancement point 2]
  - [...]
- Specific Enhancements:
  - Subplan [X]:
    - [Enhancement point 1]
    - [Enhancement point 2]
    - [...]
  - Subplan [Y]:
    - [Enhancement point 1]
    - [Enhancement point 2]
    - [...]

### Final Plan Summary:
- Number of original subplans: [X]
- Number of resulting subplans: [Y]
- Reorganization overview:
  - [Point 1]
  - [Point 2]
  - [...]
- Key observations:
  - [Observation 1]
  - [Observation 2]
  - [...]
- Recommendations:
  - [Recommendation 1]
  - [Recommendation 2]
  - [...]

### Information Preservation Check:
- [Confirmation point 1]
- [Confirmation point 2]
- [...]
- Potentially misplaced information:
  - [Item 1]: [Suggested location]
  - [Item 2]: [Suggested location]
  - [...]

### Quality Assurance Check:
- Clarity and coherence:
  - [Point 1]
  - [Point 2]
- Completeness of care needs and actions:
  - [Point 1]
  - [Point 2]
- Logical flow within sections:
  - [Point 1]
  - [Point 2]
- Consistency of terminology and phrasing:
  - [Point 1]
  - [Point 2]
- Adherence to original structure and content placement:
  - [Point 1]
  - [Point 2]
- Areas requiring further clarification or expansion:
  - [Area 1]
  - [Area 2]
  - [...]
"""
def parse_llm_response(response: str) -> Dict:
    """
    Parses the LLM response into a structured dictionary.

    Args:
    - response (str): The raw response from the LLM.

    Returns:
    - Dict: A structured representation of the response.
    """
    sections = [
        "Similarity Analysis Summary",
        "Enhanced Care Plans",
        "Reasoning and Changes",
        "FINAL_PLAN_SUMMARY"
    ]
    
    parsed_response = {}
    current_section = None
    
    for line in response.split('\n'):
        if any(section in line for section in sections):
            current_section = line.strip(':')
            parsed_response[current_section] = []
        elif current_section:
            parsed_response[current_section].append(line.strip())
    
    # Join the lines in each section
    for section in parsed_response:
        parsed_response[section] = '\n'.join(parsed_response[section]).strip()
    
    return parsed_response


global standardize_care_plan_llm
standardize_care_plan_llm = GeminiInitializer()

def final_care_plan(*subplans: str, combine_instructions: str) -> Dict:
   
    today = date.today()
    formatted_date = today.strftime("%d/%m/%y")
    print("Today's date:", formatted_date)
    formatted_subplans = "\n\n".join(f"Subplan {i+1}:\n{subplan}" for i, subplan in enumerate(subplans))

    prompt = CARE_PLAN_TEMPLATE.format(subplans=formatted_subplans, combine_instructions=combine_instructions)
    print("-----------------" * 5)
    
    response = standardize_care_plan_llm.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0)
    
    # Parse the response
    parsed_response = parse_llm_response(response)
    
    # Add original subplan count to the response
    parsed_response['original_subplan_count'] = len(subplans)
    
   #  print(json.dumps(parsed_response, indent=2))
    
    return parsed_response





