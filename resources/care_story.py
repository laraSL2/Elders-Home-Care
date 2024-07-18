import gemini_initializer 
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

def care_story_summarizer(care_story):
    care_story_prompt = CARE_STORY_SUMMARIZATION_PROMPT.format(care_story=care_story)
    gemini = gemini_initializer.GeminiInitializer() 
    _summary = gemini.extract_entities_relationships(prompt=care_story_prompt, model_name="gemini-1.5-pro-latest")
    return _summary
     
# if __name__ == '__main__':
#      care_story = """
     
#      John Doe, a 65-year-old male with a history of hypertension and Type 2 diabetes, was admitted to the hospital on June 1, 2024, with complaints of chest pain and shortness of breath. Upon arrival, his blood pressure was recorded at 160/100 mmHg, and his blood glucose level was 250 mg/dL. An electrocardiogram (ECG) revealed signs of a possible myocardial infarction (heart attack).

#      John was immediately started on aspirin and nitroglycerin to manage his chest pain, and he was given intravenous insulin to control his blood sugar levels. A cardiologist was consulted, and it was decided that John needed an emergency coronary angiography. The angiography showed a significant blockage in the left anterior descending (LAD) artery. Consequently, John underwent a successful percutaneous coronary intervention (PCI) with the placement of a drug-eluting stent.

#      Following the procedure, John was monitored in the intensive care unit (ICU) for 48 hours. His recovery was uneventful, and his blood pressure and glucose levels stabilized. He was discharged on June 5, 2024, with prescriptions for antihypertensive medications, metformin for diabetes, and a daily low-dose aspirin. John was also advised to follow a heart-healthy diet, engage in regular physical activity, and attend follow-up appointments with his cardiologist and primary care physician."""
#      print(care_story_summarizer(care_story))
