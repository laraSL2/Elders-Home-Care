import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types import HarmCategory, HarmBlockThreshold

class GeminiInitializer:
    def __init__(self):
        self.api_key = "AIzaSyB3QX46EFHbg_qL5P2QOmxZQMR5_OSCMEI"
        os.environ['GOOGLE_API_KEY'] = self.api_key
        genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

    def run_text_model(self,
        prompt: str,
        model_name: str = "gemini-1.5-pro-latest",
        temperature: float = 0
        ):
        safety_settings={HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE}
        llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature, safety_settings=safety_settings)
        response = llm.invoke(prompt)
        return response.content

    def extract_entities_relationships(self, prompt, model_name):
        try:
            res = self.run_text_model(prompt=prompt, model_name = model_name, temperature = 0)
            return res
        except Exception as e:
            print(e)