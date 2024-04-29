from gemini_initializer import GeminiInitializer

template = '''
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
   - Do not make up any sentence that doesn't convey the meaning of the Input Text. In other words meaning of the original Input Text must be preserved.
   - Refer the following examples:
      Example 1:
        Original Text: After breakfast, administer medication.
        Revised Text: Following breakfast, the caregiver will assist the resident with taking their medication.
      Example 2:
        Original Text: The patient should be encouraged to participate in physical therapy exercises.
        Revised Text: The caregiver can encourage the resident to participate in their physical therapy exercises.
      Example 3:
        Original Text: John should take his medication with meals.
        Revised Text: The caregiver should remind John to take his medication with each meal.
   - If you can't enhance the input_text, don't try to make up an answer or hallucinate. Strictly give only the paraphrased paragraph, do not give other unwanted sentences and words.
   - Evaluation criteria:
      The system will be evaluated on its ability to improve the quality of English sentences.
      Metrics for evaluation will include grammar and spelling accuracy, paraphrase fluency, and preservation of meaning.
      Evaluation will also consider the consistency of appropriate naming convention.

Therefore provide an improved version of Input Text to improve accuracy. Only provide the improved text. Do not provide any headings.

Input Text: {input_text}\n\n
Answer:
'''

def note_enhancer(text, gemini=GeminiInitializer()):
    prompt = template.format(input_text=text)
    return gemini.run_text_model(prompt, model_name="gemini-1.5-pro-latest", temperature=0.2)

