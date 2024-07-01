import os
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAI
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import HumanMessage
from rag_expert.generate_expert_suggestions import generate_suggestions,PROMPT_TEMPLATE 

import torch
from dotenv import load_dotenv
load_dotenv()

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

def get_llm_refining():
    
    try:
       
        print("loading llm")
        
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

def generate_refined_care_plan(expert_feedback,care_plan):
   
    try:
        llm = get_llm_refining()
        final_refining_prompt = FB_REFINING_TEMPLATE.format(
            expert_feedback=expert_feedback,
            generated_care_plan=care_plan
        )
        response = llm.invoke(final_refining_prompt)
        print(response)
        return response
    
    except Exception as ex:
        print(f"could not refine the care plan: {ex}")
        return "Sorry, there is some error! please try again later..."
        

REFINING_USER_INPUT = PromptTemplate(
    input_variables=["user_input_information"],
    template="""You are an expert in identifying patient personal information and medical history from given text, based on provided user information. Your task is to carefully analyze the text, extract relevant details, and make necessary adjustments according to expert feedback.

        <TEXT>
            {user_input_information}
        </TEXT>

        <INSTRUCTIONS>
            1. Thoroughly read and comprehend the given text.
            2. Identify and extract all personal and medical-related information of the patient from the provided context.
            3. Based on the given expert feedback, make necessary adjustments to the text. Remember to only work with information already present in the given text and expert feedback. Do not introduce new information or make assumptions.
            4. Maintain the original format and structure of the given text. This includes preserving any headings, bullet points, paragraphs, or other formatting elements.
            5. Do not add, remove, or modify information beyond what is explicitly stated or implied in these sources.
            6. Double-check that you have not inadvertently introduced any new information or personal interpretations.
            7. Review your work to confirm that all instructions have been followed correctly and that the refined text accurately reflects the original content with appropriate adjustments.
            8. Be mindful of patient privacy and confidentiality. Ensure that any sensitive information is handled appropriately according to medical ethics and data protection standards.
            10. If the text contains medical terminology or abbreviations, interpret them accurately and consistently throughout the document.
        </INSTRUCTIONS>

        Now, based on your expert analysis and following the above instructions, please provide:

        PERSONAL INFO:
            - All identified personal information items here
            - Include items such as name, age, gender, contact details, etc.

        MEDICAL HISTORY:
            - All identified medical history items here
            - Include items such as diagnoses, treatments, medications, allergies, etc.

        Now it is your turn... 
    """
    )

def refine_input_infomation(user_input_information, llm):
    try:
        final_refining_prompt = REFINING_USER_INPUT.format(
            user_input_information=user_input_information,
        )
        response = llm.invoke(final_refining_prompt)
        print(response)
        return response
    
    except Exception as ex:
        print(f"please try again\n {ex}")
        return "Sorry, there is some error! please try again later..."
        
        
FINAL_CARE_PLAN =PromptTemplate(
    input_variables=["personal_info","medical_history","expert_suggestions","output_template"],
    template= """You are an expert in elder care planning, tasked with creating a comprehensive care plan based on provided information. Your goal is to generate a detailed, personalized care plan that adheres to the given format and incorporates all relevant information without introducing any fictional elements.

        <PERSONAL_INFO>
            {personal_info}
        </PERSONAL_INFO>

        <MEDICAL_HISTORY>
            {medical_history}
        </MEDICAL_HISTORY>

        <EXPERT_SUGGESTIONS>
            {expert_suggestions}
        </EXPERT_SUGGESTIONS>

        <INSTRUCTIONS>
            1. Carefully review all provided information in the PERSONAL_INFO, MEDICAL_HISTORY, and EXPERT_SUGGESTIONS sections.
            2. Use this information to create a comprehensive care plan following the OUTPUT_TEMPLATE provided.
            3. Ensure that all sections of the care plan are filled with relevant, accurate information derived solely from the input data.
            4. Incorporate EXPERT_SUGGESTIONS appropriately throughout the care plan where they are most relevant, without creating a separate section for them.
            5. Present information in the format specified by the OUTPUT_TEMPLATE, maintaining a professional tone throughout.
            6. Do not introduce any information that is not explicitly stated or clearly implied by the provided inputs.
            7. If any required information is missing, indicate this in the relevant section rather than inventing details.
            8. Pay special attention to any specific care needs, medication requirements, or behavioral considerations mentioned in the inputs.
            9. Ensure that the care plan is tailored to the individual's unique circumstances as described in the PERSONAL_INFO and MEDICAL_HISTORY.
            10. Strictly adhere to the structure and formatting of the OUTPUT_TEMPLATE when generating the care plan.
            11. For each section of the care plan, generate a complete explanation using the provided parameters and present the plan in a paragraph format, ensuring coherence and clarity.
            12. Utilize the provided expert suggestions appropriately and include them in sections (Care Needs, Care Actions, Nutrition and Dietary Plan, Behaviour Monitoring Plan, etc.) where those suggestions are most suitable.
            13. Do not explicitly include expert suggestions as a separate section in the final care plan.
            14. Ensure that the generated plan adheres strictly to the provided data and format without introducing any fabricated information.
        </INSTRUCTIONS>

        <OUTPUT_TEMPLATE>
        {output_template}
        </OUTPUT_TEMPLATE>

        Now, generate a care plan using the following steps:
        <INSTRUCTIONS>
        1. Review the OUTPUT_TEMPLATE thoroughly to understand the required sections and formatting.
        2. For each section in the OUTPUT_TEMPLATE:
           a. Identify relevant information from PERSONAL_INFO, MEDICAL_HISTORY, and EXPERT_SUGGESTIONS.
           b. Compose content for that section using the identified information.
           c. Ensure the content adheres to the format specified in the OUTPUT_TEMPLATE (e.g., paragraphs, bullet points, etc.).
        3. Incorporate EXPERT_SUGGESTIONS naturally into appropriate sections of the care plan.
        4. Double-check that all sections of the OUTPUT_TEMPLATE have been addressed.
        5. Review the completed care plan to ensure it is comprehensive, coherent, and follows the OUTPUT_TEMPLATE precisely.
        6. Transform the information from the JSON format into paragraph format for each section of the care plan.
        7. Use the provided data as a guide to generate a detailed care plan without introducing any fictional elements.
        </INSTRUCTIONS>
        Please proceed with generating the care plan based on the provided inputs and following these instructions. Ensure that the plan is comprehensive, personalized, and adheres strictly to the given information and OUTPUT_TEMPLATE.
        
        Now it is your turn... 
        CARE PLAN
        """
        
)
        
def final_care_plan(plan_input_information, llm):
    try:
        response = llm.invoke(plan_input_information)

        return response
    except Exception as ex:
        print(f"please try again\n {ex}")
        return "Sorry, there is some error! please try again later..."
        
     
        
def care_plane_flow(user_input_information, expert_retriever, output_template):
    try:
        llm = get_llm_refining()
        refine_response = refine_input_infomation(user_input_information, llm)

        info = refine_response.split("PERSONAL INFO")[1].split("MEDICAL HISTORY")
        PERSONAL_INFO = info[0]
        MEDICAL_HISTORY = info[1]


        expert_suggestions = generate_suggestions(
                MEDICAL_HISTORY,
                llm,
                retriever=expert_retriever,
                template=PROMPT_TEMPLATE
            )
        print("\n\nExpert : ",expert_suggestions)

        final_care_prompt = FINAL_CARE_PLAN.format(
                personal_info=PERSONAL_INFO,
                medical_history=MEDICAL_HISTORY,
                expert_suggestions=expert_suggestions,
                output_template= output_template

            )
        care_plan = final_care_plan(final_care_prompt, llm)
        print(care_plan)
        return care_plan
    except Exception as ex:
        print(f"please try again\n {ex}")
        return "Sorry, there is some error! please try again later..."
        