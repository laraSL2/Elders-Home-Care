class Prompts:
    # Initializes the Prompts class
    def __init__(self):
        # Prompt for extracting entities and relationships related to elder, previous consultants, and previous residence
        self.eld_cons_res_prompt = """You will be given a set of particulars of a senior resident who is being admitted to a facility for the elderly, extract entities and relationships strictly as instructed below:

Three entities needed to be extracted are "Elder", "Previous_consultant", and "Previous_residence" from the elder's details.

Here are the attributes of each entity:

Elder: id, name, gender, blood_type, date_of_birth, guardian_name, guardian_contact, weight, height, bmi, english_understanding, marital_status, hobbies.
Each Elder is given an id, which is an unique identification code.
name: Elder's Full Name.
gender: Specifies the elder's gender.
blood_type: Blood varient("O+","A-",...).
date_of_birth: Date of birth of the elder.
guardian_name: Defines the primary caregiver for coordination of care.
guardian_contact: Provides contact number of the guardian.
weight: Weight of the elder.
height: Height of the elder.
bmi: Indicates the elder's body mass index.
english_understanding: Defines the language proficiency of the elder.
marital_status: Marital status of the elder.
hobbies: The elders' preference in leisure time activities.

Previous_Consultant: id, name, specialization
Each of the previous consultants are recorded with an id, which is an unique identification code.
name: name is the name of the previous consultant.
specialization: Specialization is the field of specialization of the previous consultant.

Previous_Residence: id, name, contact
The previous residence of the elder is recorded with an id, which is an unique identification code.
name: This defines the name of the previous residence of the elder.
contact: Contact details of the previous care home is the contact number or the address of the previous care home.

Data types and other properties for the above attributes should be as given below.
1) Elder
id: Primary key - String
gender: String
blood_type: String
date_of_birth: Date
guardian_name: String
guardian_contact: String
weight: Integer
height: String
bmi: Float
english_understanding: String
marital_status: String
hobbies: List[String]
2) Previous_Consultant
id: Primary key - String
name: String
specialization: String
3) Previous_Residence
id: Primary key - String
name: String
contact: String

If you cannot find any information on the entities and relationships above, return the string 'N/A'. DO NOT create any fictitious data.
DO NOT duplicate entities.
DO NOT miss out on any information related to the Elder, Previous consultants, and Previous care homeS.
DO NOT impute any missing values.
Retrieve the extracted entities and attributes from {$ctext} in a json format. Refer to the below example.
Put the "relationships" as a key with empty value in output json.
Example Output JSON:
{"entities":[{"label":"Elder","id":"elder1","name":"Sandani Sesanika","gender":"Female","blood_type":"O+","date_of_birth":"2000-09-27","guardian_name":"Kamesh Anuradha","guardian_contact":"0761234567","weight":67,"height":"175cm","bmi":120.3,"english_understanding":"Fluent Speaker","maritial_status":"Married","hobbies":["reading","hiking"]},{"label":"Previous_Consultant","id":"previous_consultant1","name":"Elijah Hoole","specialization":"Neurologist"},{"label":"Previous_Consultant","id":"previous_consultant2","name":"Kavindu Kariyawasam","specialization":"Dermatologist"},{"label":"Previous_Residence","id":"previous_residence2","name":"Manusath Uyana","contact":"0764851362"}],"relationships":[]}

Answer:"""
        # Prompt for extracting entities and relationships related to condition, disease, drug, and food
        self.con_dis_drug_food_prompt = """You will be given a set of particulars of a senior resident who is being admitted to a facility for the elderly, extract entities and relationships strictly as instructed below:

You need to extract 4 entities, namely 'Condition', 'Disease', 'Drug', and 'Food' from the elder's details.
Following are the details of the entities.
1. The 'Condition' entity is consisted of 'id', 'symptoms', 'past_diseases', and 'past_surgeries' properties.
    'symptoms': A list of symptoms the elder is currently experiencing, such as 'cough', 'skin rashes', 'running nose', etc.
    'past_diseases': History of diseases the elder has experienced in the past, such as 'cancer', 'arthritis', 'diabetes', etc.
    'past_surgeries': List of surgeries the elder has undergone previously, for example, 'knee replacement surgery', 'cataract surgery', 'gallbladder removal', elc.
2. The 'Disease' entity consists of 'id', 'name', 'level', 'identified_at', and 'description' properties.
    'name': The name of the disease.
    'level': Indicates the severity or concern level of the disease.
    'identified_at': Date when the disease was diagnosed or identified.
    'description': Additional information describing the disease's impact on the elder.
3. The 'Drug' entity consists of 'id', 'name', 'dosage', 'frequency', and 'identifier_code'.
    'name': The name of the drug, such as 'amoxicillin', 'losartan', or 'lisinopril'.
    'dosage': The prescribed amount of the drug to be administered, for example, '5ml', '10ml', '2 pills', or '1 pill'.
    'frequency': How often the drug should be taken, such as 'once a day' or 'twice per day'.
    'identifier_code': A code used to identify the drug, typically for purchase or tracking purposes.
4. The 'Food' entity consists of 'id', 'name', 'description', "allergy" and "prefer".
    'name': The name of the food.
    'description': Details about the food and its relevance to the elder's dietary needs or restrictions.
    'allergy': Indicates whether the food item may cause an allergic reaction for the elder.
    'prefer': Describes the elder's preferences or dietary restrictions regarding the food.
Strictly follow these Guidelines:
1. First, look for the properties in each entity and extract them.
    `id` properties of each entity must be alphanumeric and must be unique among the entities. You will be referring to this property to define the relationship between entities. NEVER create new entity types that aren't mentioned above. You will have to generate as many entities as needed as per the types below:
    entities Types:
        label:'Condition',id:string,symptoms:list[string],past_diseases:list[string],past_surgeries:list[string]
    label:'Disease',id:string,name:string, level:integer,identified_at:string,description:string
    label:'Drug',id:string,name:string,name:string,dosage:string,frequency:string,identifier_code:string
    label:'Food',id:string,name:string,description:string,allergy:"True" or "False",prefer:"True" or "False"
2. Next generate each relationship as triples of head, relationship, and tail. To refer to the head and tail entities, use their respective `id` property. NEVER create new Relationship types that aren't mentioned below:
    disease1|HAS_DRUG|drug1
    disease1|NOT_RECOMMENDED|food1
    disease1|RECOMMENDED|food2
3. If you cannot find any information on the entities and relationships above, return the string 'N/A'. DO NOT create any fictitious data.
4. Do NOT create duplicate entities.
6. DO NOT MISS out on any Medical condition, Diseases, Medical Drugs, and Foods related information.
7. DO NOT impute any missing values.

Example Output JSON:
{"entities":[{"label":"Condition","id":"condition1","symptoms":["cough","skin_rashes","running_nose"],"past_diseases":["cancer","arthritis"],"past_surgeries":["knee_replacement_surgery","cataract_surgery"]},{"label":"Disease","id":"disease1","name":"diabetes","level":4,"identified_at":"2024-01-25","description":"diabetes is the main disease of this elder."},{"label":"Drug","id":"drug1","name":"amoxicillin","dosage":"500 mg","frequency":"two times per day","identifier_code":"ANX1020"},{"label":"Food","id":"food1","name":"Rice and Fish Curry","description":"Like to eat fish curry with high spicy.","allergy":"False","prefer":"True"},{"label":"Food","id":"food2","name":"Pork","description":"Experiencing rashes after eating","allergy":"True","prefer":"False"}],"relationships":["disease1|HAS_DRUG|drug1","disease1|NOT_RECOMMENDED|food2","disease1|RECOMMENDED|food1"]}

Question: Now, extract entities & relationships as mentioned above for the text below -
$ctext

Answer: """
        # Prompt for extracting entities and relationships related to monitoring plan, observation, and doctor schedule
        self.mon_obs_docshe_prompt = """You will be given a set of particulars of a senior resident who is being admitted to a facility for the elderly, extract entities and relationships strictly as instructed below:

Three entities needed to be extracted are Monitoring_Plan, Observation, and Doctor_Schedule from the elder's details.

Here are the attributes of each entity:

1) Monitoring_Plan: id, parameter, frequency, start_date, end_date, start_time, end_time
a) Each Monitoring_Plan has an id, which is an unique identification code.
b) The parameter property specifies what aspect of the elder's health needs monitoring, for example, "checking the temperature."
c) frequency indicates how often the parameter should be monitored. (ex: "in every 6 hours")
d) start_date and end_date denote the start and end dates of the monitoring plan, respectively.

2) Observation: id, description, date, time
a) Each Observation is recorded with an id, which is an unique identification code.
b) description describes the observation made, such as "Hemoglobin is Low."
c) date signifies the date when the observation was recorded.

3) Doctor_Scheduled: id, doctor_name, hospital_name, appoinment_date, appointment_time, prerequisites
a) Each Appointment is recorded with an id, which is an unique identification code.
b) doctor_name denotes the name of the attending doctor.
c) hospital_name specifies the name of the hospital where the appointment is scheduled.
d) appoinment_date and appointment_time indicate the date and time of the scheduled appointment.
c) prerequisites entail any instructions or tests that need to be followed or completed before meeting the doctor.

Data types and other properties for the above attributes should be as given below.
1) Monitoring_Plan
id: Primary key - String
parameter: String
frequency: String
start_date: String
start_time: time
end_date: String
end_time: time
2) Observation
id: Primary key - String
description: String
date: String
time: time
3) Doctor_Scheduled
id: Primary key - String
doctor_name: String
hospital_name: String
appoinment_date: String
appointment_time: Time
prerequisites: String

Generate relationships among the entities in triples as below. Adhere to following relationship types only. Do not make any new relationships that aren’t mentioned below.
doctor_scheduled|NEEDS_OBSERVATION|observation
doctor_scheduled|NEEDS_MONITORING|monitoring_plan
If you cannot find any information on the entities and relationships above, return the string 'N/A'. Do not create any fictitious data.
Do not duplicate entities.
Do not miss out on any information related to Monitoring, Observation, and Doctor Schedules/appoinments.
Do not impute any missing values.
Retrieve the extracted entities and attributes from {$ctext} in a json format. Refer to the below example.
{"entities":[{"label":"Monitoring_Plan","id":"monitoring_plan1","parameter":"check blood pressure","frequency":"once a day","start_date":"2021-01-01","end_date":"2022-02-01","start_time":"20:24:00","end_time":"03:45:00"},{"label":"Observation","id":"observation1","finding_name":"Eye sight is low","Date":"2020-01-01","time":"21:24:00"},{"label":"Doctor_Scheduled","id":"doctor_scheduled1","doctor_name":"Kamesh Anuradha","hospital_name":"Colombo main Hospital","appoinment_date":"2024-03-24","appoinment_time":"10:00:00","prerequisites":"don't eat any food before meet the doctor"},{"label":"Observation","id":"observation2","finding_name":"blood pressure is high","date":"2024-01-01","time":"11:24:00"}],"relationships":["doctor_scheduled1|NEEDS_OBSERVATION|observation2","doctor_scheduled1|NEEDS_MONITORING|monitoring_plan1"]}

answer:
"""
        # Prompt for extracting entities related to ADL, IADL, Cognitive Assessment, and Social History
        self.adl_iadl_cog_soc_prompt = """You will be given a set of particulars of a senior resident who is being admitted to a facility for the elderly, extract entities strictly as instructed below:

Three entities needed to be extracted are "ADL" (Activities of Daily Livings), "IADL" (Instrumental Activities of Daily Livings), "Cognitive_Assessment" and "Social_History" from the elder's details.

Here are the attributes of each entity:

1) ADL: id, description
a) Each ADL has an id, which is an unique identification code.
b) The "description" property specifies what activities of daily livings of the elder required to assist. As an example a elder needs help for bath, eat, toileting, such things.

2) IADL: id, description
a) Each IADL is recorded with an id, which is an unique identification code.
b) "description" describes the instrumental activities of daily livings of the elder required to assist. As an example a elder needs help with using phone, bathroom accessories, medication management, managing finances such things.

3) Cognitive_Assessment: id, description
a) Each Cognitive_Assessment is recorded with an id, which is an unique identification code.
b) "description" describes the issues in elder's brain’s ability to process information from the senses. As an example the issues with Thinking, Learning, Understanding and using language, Remembering, Paying Attention, Reasoning, Making decisions such things.

4) Social_History: id, smoking, alcohol, drug_use, past_occupation, family_history, abuse, legal_issues, education, end_of_life, other
a) for above all the properties include the relavent past details for that elder. As an example "family_history" has value "wife and three children" such things.

Data types and other properties for the above attributes should be as given below.
1) ADL
id: Primary key - String
description: String
2) IADL
id: Primary key - String
description: String
3) Cognitive_Assessment
id: Primary key - String
description: String
4) Social_History
id: Primary key - String
smoking: String
alcohol: String
drug_use: String
past_occupation: List[String]
family_history: String
abuse: String
legal_issues: List[String]
education: String
end_of_life: String
other: String

If you cannot find any information on the entities above, return the string 'N/A'. DO NOT create any fictitious data.
DO NOT duplicate entities.
DO NOT miss out on any information related to Monitoring, Observation, and Doctor Schedules.
DO NOT impute any missing values.
Do not put '," characters into the properties string. As an example, use "womens" instead of "women's".
In output json PUT "relationships" key with empty List.
Retrieve the extracted entities and attributes from {$ctext} in a json format. Refer to the below example.
{"entities":[{"label":"ADL","id":"ADL1","description":"needs assistance with eating and bathing."},{"label":"IADL","id":"IADL1","description":"needs assistance with using phone and television"},{"label":"Cognitive_Assessment","id":"cognitive_assessment1","description":"very anxious person and takes decisions quickly"},{"label":"Social_History","id":"social_history1","smoking":"heavily smoker 20 years ago","alcohol":"Not used","drug":"drug used in young age","past_occupation":["teacher","farmer"],"family_history":"wife and two children","abuse":"No","legal_issues":["participated in a bank robbery in 2007","stolen womens handbag"],"education":"has a diploma","end_of_life":"needs to go on an India tour","other":"has participated in many blood donations"}],"relationships":[]}

answer:
"""

    def plan_prompt(
            self,
            elderID,
            elder_data,
            social_history,
            medical_history,
            functional_status,
            outings,
            disease_data,
            drug_data,
            dietary_plan,
            monitoring_plan,
            doctor_schedule,
            care_notes,
            rag_suggestions
        ):
        # Generates a comprehensive care plan based on the provided data
        plan_prompt = f"""Using the provided data parameters regarding an elder admitted to a new care facility, generate a comprehensive care plan in the specified format.

For each section of the care plan, You should generate a complete explanation using the provided parameters and present the plan in a paragraph format, ensuring coherence and clarity. You must \
utilize the provided rag suggestions approriately and include them in sections (Care Needs, Care Actions, Nutrition and Dietary Plan, Behaviour Monitoring Plan, etc.) where those suggestions are most suitable. You must not explicitly include rag suggestions as a separate section in the final care plan.

RAG SUGGESTIONS: {rag_suggestions}

Ensure that the generated plan adheres strictly to the provided data and format without introducing any fabricated information.

Below, you'll find the care plan template along with the necessary data for each section provided in JSON format. Your task is to transform this information into paragraph format.


Profile Details and Background

Elder ID: {elderID}
Full Name:
Age:
Gender:
Elder data: {elder_data}


----------------------------------------


Care Needs:
List down all care needs of the respective elder. Utilize information from {functional_status}, {outings}, {disease_data}, and {monitoring_plan} to give a detailed set of needs.
Give in point format. Take {elder_data} into consideration, when formulating sentences. 


Care Actions:
List down all care actions taken by care givers in taking care of the elder. Utilize information from {care_notes} into generating content for this section.
Describe each in paragraphs. Take {elder_data} into consideration, when formulating sentences. 


Outcome/ Goal:
Give a brief summary of {care_notes} as an overall goal for the specific elder. Be precise.


-------------------------------


Social History
This section details the elder's background and current living situation. It includes their past and present occupation, current living arrangements, and any previous residences.
Social History data: {social_history}


Medical History
Detail the elder's current medical condition, previous consultations, medication plan adherence, past diseases, and surgeries. Provide a thorough account of the elder's medical journey to date.
Medical history data: {medical_history}


Functional Status with Assessments
Assess the elder's ability to perform daily tasks, including Activities of Daily Living (ADL), Instrumental Activities of Daily Living (IADL), and cognitive assessments. Describe the elder's functional status based on these assessments.
Functional Status data: {functional_status}


Outings and Activities Plan
Tailor the elder's outings and activities plan to incorporate enjoyable activities into their routine while considering any activity restrictions due to medications. Promote physical and mental well-being through engaging activities.
outings_data: {outings}


Diseases
Provide detailed descriptions of the elder's diseases, including names, identification dates, descriptions, and related drug treatments. Ensure clarity and specificity in presenting this information.
Disease data: {disease_data}


Medication Plan
Explain the elder's medication regimen, including drug names, dosages, frequencies, and any additional details. Ensure clarity and accuracy in conveying this vital information.
Drugs Data: {drug_data}


Nutrition and Dietary Plan
Tailor the elder's nutrition and dietary plan to meet their specific needs, preferences, and allergies. Consider recommended and not recommended foods for the elder's conditions to ensure optimal health.
Nutrition and Dietary Plan data: {dietary_plan}


Behaviour Monitoring Plan
Detail observations made for the elder and specify monitoring needs. Emphasize the importance of monitoring for changes in behavior or health status and outline the necessary actions.
Monitoring Plan: {monitoring_plan}


Doctor Schedules
List upcoming doctor appointments with specialists, noting any prerequisites or monitoring requirements. Ensure that the elder's health is closely monitored and managed through these appointments.
doctor schedule data: {doctor_schedule}

Summarization of Previous Care Notes
In this Section You need to summariza the information contains in the care notes provided below in JSON format. If there is important thing in a care note add the date of the care note as well for that thing.
care_notes: {care_notes}

----------------------------------------

Use this as a guide to generate a detailed care plan based on the provided data without introducing any fictional elements.
Care Plan:
"""
        return plan_prompt