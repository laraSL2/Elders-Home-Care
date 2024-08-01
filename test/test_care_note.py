import requests
import json
import time
from datetime import datetime
import random

# The URL of your Flask server
URL = "http://127.0.0.1:8001/note_enhancement"

# # List of 50 example care notes
# care_notes = [
#     "Resident performed ADLs, needed minimal assist with dressing. Appetite good, ate 75% of meal.",
#     "LISINOPRIL 10mg tablets. Quantity given: 1.00. Directions: Take ONE tablet daily.",
#     "During dinner, resident became agitated and yelled at staff, using profanity. Refused to eat meal.",
#     "Resident slept well through the night. No issues reported.",
#     "Administered insulin 10 units subcutaneously before breakfast as per order.",
#     "Resident participated in group exercise. Showed improved mobility.",
#     "Changed wound dressing on left leg. Area looks clean, no signs of infection.",
#     "Resident confused this morning, unable to recognize family members during visit.",
#     "Fall incident: Resident found on floor in bathroom. No visible injuries. Protocol followed.",
#     "Resident resistant to morning care, pushed caregiver away. Required two staff to assist.",
#     "Blood pressure reading: 130/80 mmHg. Within normal range for resident.",
#     "Resident enjoyed music therapy session, appeared more relaxed afterwards.",
#     "Administered PRN pain medication for back pain. Resident reported relief after 30 minutes.",
#     "Resident refused to take evening medications. Reason unclear.",
#     "Noticed small bruise on resident's right arm. Origin unknown, will monitor.",
#     "Resident very talkative during lunch, shared stories about childhood.",
#     "Assisted resident with video call to family. Mood improved noticeably after call.",
#     "Resident complained of feeling cold. Provided extra blanket and adjusted room temperature.",
#     "Encouraged fluid intake throughout day. Resident drank approximately 1000ml.",
#     "Resident became tearful when discussing deceased spouse. Provided emotional support.",
#     "Administered nebulizer treatment as prescribed. Resident's breathing improved.",
#     "Resident agitated during personal care, yelled at staff. Calmed down after 15 minutes.",
#     "Noticed resident limping slightly. Will inform physiotherapist for assessment.",
#     "Resident enjoyed gardening activity, potted three plants with minimal assistance.",
#     "WARFARIN 5mg tablet given as per INR result. Next INR check scheduled for Friday.",
#     "Resident slept fitfully, got up multiple times during night. Will monitor for pattern.",
#     "Morning blood sugar reading: 7.2 mmol/L. Within target range.",
#     "Resident refused breakfast, complaining of nausea. Administered prescribed anti-emetic.",
#     "Observed resident talking to self, appeared distressed. Redirected with calm conversation.",
#     "Resident had a visitor today. Mood noticeably improved after visit.",
#     "Changed catheter bag. Urine clear, output within normal range.",
#     "Resident attended art therapy. Created a painting of childhood home.",
#     "Administered eye drops for glaucoma as prescribed. No issues noted.",
#     "Resident reported chest pain. EKG performed, doctor notified as per protocol.",
#     "Encouraged resident to use walker, but refused. Will continue to encourage for safety.",
#     "Resident enjoyed outdoor walk in garden. Oxygen saturation remained stable.",
#     "Administered oral antibiotics for UTI as prescribed. Reminded resident about fluid intake.",
#     "Resident became aggressive during shower, attempted to hit caregiver. Used de-escalation techniques.",
#     "Facilitated resident's attendance at facility's birthday celebration. Resident participated actively.",
#     "Resident complained of loneliness. Spent extra time engaging in conversation about family photos.",
#     "Performed range of motion exercises with resident. Noted increased flexibility in left arm.",
#     "Resident had episode of shortness of breath. Oxygen applied, doctor notified.",
#     "Assisted resident with choosing outfit for day. Resident expressed satisfaction with independence.",
#     "Resident refused dinner, stating no appetite. Offered alternative snacks.",
#     "Administered prescribed antidepressant. Will monitor for side effects and mood changes.",
#     "Resident had a nosebleed. Applied first aid, bleeding stopped after 10 minutes.",
#     "Observed resident reading book independently. Cognitive function appears stable.",
#     "Resident expressed anxiety about upcoming medical appointment. Provided reassurance and information.",
#     "Administered insulin sliding scale as per blood sugar reading of 11.2 mmol/L.",
#     "Resident displayed sundowning behavior in evening. Used calming techniques as per care plan."
# ]

complex_care_notes = [
    # Normal Care (20 cases)
    "Resident assisted with shower, minimal help needed. Skin intact, no concerns noted.",
    "Encouraged fluids throughout shift. Resident consumed approximately 1000ml of water.",
    "Resident participated in group exercise class. Showed improved balance during standing exercises.",
    "Changed wound dressing on left shin. Area appears to be healing well, no signs of infection.",
    "Resident enjoyed virtual reality session, exploring a beach scene. Appeared more relaxed afterwards.",
    "Assisted with nail care. Resident chose red polish for fingernails.",
    "Resident used walker for ambulation to dining room. Gait steady, no falls.",
    "Engaged resident in reminiscence therapy using old photographs. Shared stories about childhood.",
    "Performed range of motion exercises. Noted increased flexibility in right shoulder.",
    "Resident attended music therapy session. Actively participated by singing along to familiar songs.",
    "Assisted with teeth brushing. Resident able to hold brush but needed help with toothpaste application.",
    "Encouraged use of hearing aids. Resident more engaged in conversations when wearing them.",
    "Resident participated in art therapy. Created a watercolor painting of a sunset.",
    "Assisted with hair combing and styling. Resident expressed satisfaction with appearance.",
    "Encouraged resident to make choices about daily outfit. Selected blue shirt and gray pants.",
    "Resident used bedside commode independently. Proper hand hygiene performed afterwards.",
    "Assisted with applying moisturizer to dry skin areas. Resident reported feeling more comfortable.",
    "Engaged resident in cognitive stimulation activities. Completed a crossword puzzle with minimal assistance.",
    "Resident participated in gardening activity. Potted three plants with guidance.",
    "Assisted with repositioning in bed every 2 hours. No skin breakdown observed.",

    # Medication-Related (20 cases)
    "LISINOPRIL 10mg tablets. Quantity given: 1.00. Directions: Take ONE tablet daily in the morning.",
    "Administered insulin 10 units subcutaneously before breakfast as per sliding scale. Blood sugar was 180 mg/dL.",
    "WARFARIN 5mg tablet given. INR result: 2.5. Next check scheduled for Friday.",
    "LEVOTHYROXINE 50mcg tablets. Quantity given: 1.00. Directions: Take ONE tablet daily on an empty stomach.",
    "Resident refused evening dose of QUETIAPINE 25mg. Reason given: 'Don't want to feel groggy.'",
    "METFORMIN 500mg tablets. Quantity given: 2.00. Directions: Take TWO tablets twice daily with meals.",
    "Administered PRN ACETAMINOPHEN 500mg for complaints of back pain. Pain level reduced from 7/10 to 3/10 after 1 hour.",
    "AMLODIPINE 5mg tablets. Quantity given: 1.00. Directions: Take ONE tablet daily. BP before administration: 150/90 mmHg.",
    "LATANOPROST 50mcg/ml eye drops. Administered ONE drop in each eye at bedtime.",
    "Resident complained of difficulty swallowing POTASSIUM CHLORIDE tablet. Switched to liquid form as per doctor's order.",
    "DONEPEZIL 10mg tablets. Quantity given: 1.00. Directions: Take ONE tablet at bedtime. Resident reported vivid dreams.",
    "FUROSEMIDE 40mg tablets. Quantity given: 1.00. Directions: Take ONE tablet in the morning. Encouraged fluid intake.",
    "Administered ALBUTEROL 2.5mg via nebulizer for shortness of breath. O2 saturation improved from 92% to 97%.",
    "METOPROLOL 25mg tablets. Quantity given: 1.00. Directions: Take ONE tablet twice daily. Pulse rate: 68 bpm.",
    "CLOPIDOGREL 75mg tablets. Quantity given: 1.00. Directions: Take ONE tablet daily. Monitored for any unusual bruising.",
    "Resident refused SENNA 8.6mg tablets, citing stomach discomfort. Offered prune juice as alternative.",
    "RISPERIDONE 0.5mg tablets. Quantity given: 1.00. Directions: Take ONE tablet twice daily. Monitored for extrapyramidal symptoms.",
    "Administered LORAZEPAM 0.5mg as needed for anxiety before medical appointment. Resident appeared calmer after 30 minutes.",
    "GABAPENTIN 300mg capsules. Quantity given: 1.00. Directions: Take ONE capsule three times daily. Resident reported reduced nerve pain.",
    "SIMVASTATIN 20mg tablets. Quantity given: 1.00. Directions: Take ONE tablet at bedtime. Reminded resident about grapefruit juice interaction.",

    # Behavioral Concerns (30 cases)
    "Resident became agitated during evening care, refusing to change clothes. Calmed after 20 minutes of reassurance and offering choices.",
    "Observed resident pacing in hallway, appearing confused. Gently redirected back to room and oriented to time and place.",
    "Resident exhibited signs of sundowning, becoming restless and anxious as evening approached. Implemented calming routine with soft music and dimmed lights.",
    "During meal time, resident became frustrated and pushed plate away. Offered alternative food choices and encouraged independence in feeding.",
    "Resident reluctant to participate in morning hygiene routine. Used picture cards to explain process, resident then cooperated.",
    "Observed resident attempting to exit facility. Redirected with conversation about family photos, resident became more settled.",
    "Resident expressed paranoid thoughts about staff 'stealing' belongings. Validated feelings and conducted room search together to alleviate concerns.",
    "During group activity, resident became verbally disruptive, speaking loudly and off-topic. Offered one-on-one activity in quieter space.",
    "Resident refused to take shower, expressing fear of water. Used bed bath method with resident's cooperation.",
    "Observed resident hoarding food items in room. Gently explained concerns and worked with resident to sort through items.",
    "Resident showed signs of depression, refusing to leave room for activities. Encouraged brief visits from preferred staff members.",
    "During night check, found resident awake and anxious about upcoming doctor's appointment. Provided reassurance and reviewed appointment details.",
    "Resident became upset when favorite chair was occupied. Offered alternative seating and distracted with preferred activity.",
    "Observed resident exhibiting inappropriate sexual behavior towards staff. Redirected with firm but respectful boundary setting.",
    "Resident refused to use walker, insisting on walking independently despite fall risk. Negotiated compromise of using walker in hallways only.",
    "During personal care, resident became tearful and uncooperative. Took breaks as needed and used distraction techniques.",
    "Resident displayed obsessive behavior, repeatedly folding and unfolding clothes. Redirected to sorting activity with laundry staff.",
    "Observed resident scratching skin excessively. Applied moisturizer and provided stress ball as alternative sensory stimulation.",
    "Resident became agitated when room temperature was adjusted. Compromised by providing extra blanket instead.",
    "During meal time, resident insisted on eating with hands despite capability to use utensils. Offered finger foods as part of meal to maintain dignity.",
    "Resident refused to take medications, expressing distrust. Took time to explain each medication and its purpose, resident then complied.",
    "Observed resident attempting to disrobe in common areas. Gently redirected to private space and assisted with comfortable clothing.",
    "Resident became anxious and combative during transfer from bed to chair. Paused process, explained steps, and proceeded slowly with resident's cooperation.",
    "During family visit, resident became emotionally overwhelmed and asked visitors to leave. Provided support and gradually reintroduced visitors in shorter sessions.",
    "Resident exhibited loud vocalizations during quiet hours, disturbing others. Investigated for pain or discomfort, then used music therapy to soothe.",
    "Observed resident collecting and hiding facility items in room. Worked with resident to create a personal 'treasure box' of safe items to collect.",
    "Resident resisted tooth brushing, clenching jaw shut. Used modeling technique and flavored toothpaste to encourage cooperation.",
    "During transport to appointment, resident became anxious and attempted to unbuckle seatbelt. Used calming conversation and stress ball to reduce anxiety.",
    "Resident expressed suspicion about medication, insisting it was poison. Involved resident in pill identification process with pharmacist to alleviate concerns.",
    "Observed resident repetitively opening and closing drawers, appearing distressed. Provided purposeful activity of sorting colored items to redirect behavior.",

    # Aggression (30 cases)
    "During morning care, resident became physically aggressive, attempting to hit caregiver. Required two staff to safely complete care.",
    "Resident yelled profanities at staff and other residents during dinner. Removed from dining area to prevent escalation.",
    "While ambulating in hallway, resident suddenly pushed another resident unprovoked. Immediately separated individuals and assessed for injuries.",
    "During medication administration, resident knocked medication cup out of nurse's hand and threatened to 'punch' if approached again.",
    "Resident became combative during shower, kicking and scratching caregivers. Shower terminated for safety, will attempt later with different approach.",
    "In common area, resident threw chair across room, nearly hitting another resident. Quickly evacuated area and implemented de-escalation techniques.",
    "Resident spat at caregiver during oral care and attempted to bite hand. Care suspended, will consult with dental hygienist for alternative approaches.",
    "During night check, found resident attempting to strangle roommate. Immediately separated residents and called for medical evaluation.",
    "Resident brandished cane as weapon, swinging at staff who approached. Used verbal de-escalation from a safe distance.",
    "In an agitated state, resident barricaded self in room and threatened harm to anyone entering. Implemented crisis protocol and contacted physician.",
    "During group activity, resident suddenly overturned table and began throwing objects at others. Evacuated other residents and contained situation.",
    "Resident became violent when asked to change soiled clothing, punching caregiver in face. Suspended care and implemented two-person care plan.",
    "While in garden area, resident uprooted plants and threw soil at staff. Redirected other residents indoors and used calm approach to de-escalate.",
    "During physical therapy session, resident kicked therapist and attempted to push over equipment. Session terminated, will reassess approach.",
    "Resident entered another resident's room and became physically aggressive when asked to leave. Required staff intervention to safely remove.",
    "In dining area, resident stabbed another resident's hand with fork. Immediately separated individuals and provided first aid.",
    "Resident had violent outburst during family visit, throwing objects and making threats. Escorted family to safe area and implemented crisis plan.",
    "During medication round, resident slapped medication tray from nurse's hands and shoved nurse against wall. Suspended med pass and called for assistance.",
    "Resident attempted to push housekeeping staff down stairs. Immediately implemented fall prevention protocol and removed cleaning cart from area.",
    "In a confused state, resident struck out at multiple staff members, causing minor injuries. Implemented team approach for safe management.",
    "Resident became extremely agitated during personal care, biting caregiver's arm. Care suspended, wound treated, and behavior management plan reviewed.",
    "During meal time, resident threw hot coffee at another resident. Promptly addressed burns and separated individuals.",
    "Resident had aggressive outburst in TV room, breaking television and threatening others with broken pieces. Evacuated area and called for emergency assistance.",
    "While on community outing, resident became combative on bus, attempting to open emergency exit. Terminated outing and returned to facility with additional staff support.",
    "Resident cornered and physically threatened a visibly frightened caregiver. Other staff intervened to ensure caregiver's safety and calm resident.",
    "During physical confrontation with another resident, individual picked up and threw a chair. Staff intervened to separate residents and secure area.",
    "Resident violently resisted vital sign check, knocked over medical cart, and scattered supplies. Suspended routine checks and consulted with physician for alternative monitoring.",
    "In an agitated state, resident attempted to push over large bookcase in common area, endangering nearby residents. Staff quickly intervened to prevent injury and property damage.",
    "During night shift, resident exited room and began banging on other residents' doors, becoming physically aggressive when redirected. Implemented night security protocol.",
    "Resident had severe reaction to bathing, screaming and striking out at multiple caregivers. Suspended bathing and consulted with behavioral specialist for new care plan."
]


def write_output(file, key, value, indent=0):
    if isinstance(value, dict):
        file.write(f"{'  ' * indent}{key}:\n")
        for sub_key, sub_value in value.items():
            write_output(file, sub_key, sub_value, indent + 1)
    elif isinstance(value, list):
        file.write(f"{'  ' * indent}{key}:\n")
        for item in value:
            file.write(f"{'  ' * (indent + 1)}- {item}\n")
    else:
        file.write(f"{'  ' * indent}{key}: {value}\n")

def test_care_note_enhancement(care_note, file):
    payload = {"care_note": care_note}
    response = requests.post(URL, json=payload)
    
    file.write(f"Original: {care_note}\n")
    file.write(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        result = response.json()
        print(result)
        print("\n\n")
        
        if isinstance(result, dict):
            for key, value in result.items():
                write_output(file, key, value)
        else:
            file.write(f"Unexpected result format: {result}\n")
    else:
        error_message = response.json().get('error', 'Unknown error occurred')
        file.write(f"Error: {error_message}\n")
    
    file.write("---"*50)
    file.write("\n\n")

def main():
    start_time = time.time()
    
    # Create a filename with the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test/care_note_test_results_2.txt"
    
    with open(filename, 'w') as file:
        for i, care_note in enumerate(complex_care_notes, 1):
            print(f"Test {i}/50:")
            file.write(f"Test {i}/50:\n")
            test_care_note_enhancement(care_note, file)
            time.sleep(10)
    
    end_time = time.time()
    
    with open(filename, 'a') as file:
        file.write(f"\nTotal time taken: {end_time - start_time:.2f} seconds\n")
    
    print(f"Test results have been written to {filename}")

if __name__ == "__main__":
    random.shuffle(complex_care_notes)
    main()