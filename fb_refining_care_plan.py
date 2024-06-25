
import os
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAI


from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import HumanMessage

import torch


from dotenv import load_dotenv
load_dotenv()

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

FB_REFINING_TEMPLATE = PromptTemplate(
    input_variables=["generated_care_plan","expert_feedback"],
    template="""You are an expert in reveiwing and correcting the given text based on the provided feedback. 
    
    <TEXT>
        {generated_care_plan}
    </TEXT>
    
    <INSTRUCTIONS>
        1. Read and understand the given text.
        2. Analyze and understand the given expert feedback.
        3. Based on the given expert feedback do the necessary adjustment in the given text. Remember not to add additional things out from the already given text and provided expert text. 
        4. Avoid changing the original format/design of the given text. You are only allowed to do the necessary changes based on the provided expert feedback. 
        5. It is your job to identify the relevant places which is required changes in the given text based on the analysis performed on expert feedback.
        6. Make sure you do not add additional information by your own apart from the expert feedback or given text.
        7. Make sure you followed all the instructions correctly and give refined text.  
    </INSTRUCTIONS>
    
    Now it is your turn...
    
    <EXPERT FEEDBACK>
        {expert_feedback}
    </EXPERT FEEDBACK>
    
    REFINED_FEEDBACK:
    """
    )
def get_llm_refining():
    
    try:
       
        print("loading llm for refining generated care plan")
        
        refining_llm =  GoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0,
            top_k=3,
            top_p=0.7,
            max_output_tokens=1048,
            # safety_settings=gemini_safety_settings,
        )
        
        return refining_llm

    except Exception as ex:
        
        print("error in loading refining llm: ",ex)
      


def generate_refined_care_plan(expert_feedback,care_plan,refining_llm):
   
    try:
        final_refining_prompt = FB_REFINING_TEMPLATE.format(
            expert_feedback=expert_feedback,
            generated_care_plan=care_plan
        )
        response = refining_llm.invoke(final_refining_prompt)
        
        return response
    
    except Exception as ex:
        print(f"could not refine the care plan: {ex}")
        return "Sorry, there is some error! please try again later..."
        
# def main():
#     retriever_from_llm,expert_llm = get_llm_and_retriever()
    
#     while True:
        
#         user_query = input("Patient medical details: ")
#         print()
        
#         if user_query == "exit":
#             break
            
        
#         response = generate_suggestions(
#             user_query,
#             expert_llm,
#             retriever=retriever_from_llm,
#             template=PROMPT_TEMPLATE
#         )
        
#         print(response)
#         print("-"*100)

# if __name__=="__main__":
#     main()