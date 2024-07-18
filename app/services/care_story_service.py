from flask import current_app
from langchain.prompts import PromptTemplate

CARE_STORY_SUMMARIZATION_PROMPT = PromptTemplate(
    input_variables=["care_story"],
    template="""You are an expert in summarizing medical care stories. Your task is to carefully analyze the given care story and provide a concise summary.
    
    <CARE STORY>
        {care_story}
    </CARE STORY>

    <INSTRUCTIONS>
        1. Thoroughly read and comprehend the given care story.
        2. Use clear, professional medical language while keeping the summary accessible to non-medical readers.
        3. Be objective and factual in your summary, avoiding personal interpretations or assumptions.
        4. If the story contains medical terminology or abbreviations, interpret them accurately and provide brief explanations if necessary.
        5. Ensure the summary is comprehensive yet concise.
        6. Double-check your work to confirm all instructions have been followed and the summary accurately reflects the original care story.
    </INSTRUCTIONS>

    Based on your expert analysis and following the above instructions, please provide a summary of the care story using this structure:

    CARE_STORY_SUMMARY:
    """
)

def summarize_care_story(care_story: str) -> str:
    gemini = current_app.gemini
    care_story_prompt = CARE_STORY_SUMMARIZATION_PROMPT.format(care_story=care_story)
    summary = gemini.extract_entities_relationships(prompt=care_story_prompt, model_name="gemini-1.5-pro-latest")
    return summary