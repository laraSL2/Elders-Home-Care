import os
import json
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

class GeminiInitializer:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get('GOOGLE_API_KEY')
        genai.configure(api_key=self.api_key)
        print("Initializing the model")

    def run_text_model(self,
        prompt: str,
        model_name: str = "gemini-1.0-pro",
        temperature: float = 0
        ):
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE
        }
        llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature, safety_settings=safety_settings)
        response = llm.invoke(prompt)
        return response.content

    def extract_entities_relationships(self, prompt, model_name):
        try:
            res = self.run_text_model(prompt=prompt, model_name=model_name, temperature=0)
            return res
        except Exception as e:
            print(e)
            return None