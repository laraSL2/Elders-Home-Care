from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
import json
import streamlit as st
from streamlit_option_menu import option_menu
from care_note_enhancement import note_enhancer
from care_plan_generator import generate_plan
from knowledge_graph import add_patient, get_next_patient_id
from gemini_initializer import GeminiInitializer
from graph_initializer import GraphInitializer
import textwrap as tw
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from io import BytesIO
import base64
from retrive_ids import getID, get_elder_details
from sqlite_db  import ElderDB, CarePlanDB, CareNoteDB

def get_image_as_base64(url):
    with open(url, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


### temperory expert
from rag_expert.generate_expert_suggestions import get_llm_and_retriever

if "mv_retriever" not in st.session_state and "expert_llm" not in st.session_state:
    st.session_state.mv_retriever,st.session_state.expert_llm = get_llm_and_retriever()
####

### care plan refining llm
from fb_refining_care_plan import get_llm_refining,generate_refined_care_plan

if "refining_llm" not in st.session_state:
    st.session_state.refining_llm = get_llm_refining()

###

my_gemini = GeminiInitializer()
my_graph = GraphInitializer()
ids_container = getID()
elderDB = ElderDB("database/elder_db.db")
carePlanDB = CarePlanDB("database/care_plane_db.db")
careNoteDB = CareNoteDB(("database/care_note_db.db"))

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

def create_pdf(content):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    Story = []

    styles = getSampleStyleSheet()

    sections = content.split("**")

    for index, section in enumerate(sections):
        if section.strip():
            if index == 0: 
                ptext = '<font size=20 color="red"><b>%s</b></font>' % section.strip()
                ptext = ptext.replace("#","")
                Story.append(Paragraph(ptext, styles["Heading1"]))
            elif section[-1] == ":":
                ptext = '<font size=14 color="blue"><b>%s</b></font>' % section.strip()
                Story.append(Paragraph(ptext, styles["Heading2"]))
            else:
                ptext = '<font size=12>%s</font>' % section.strip()
                Story.append(Paragraph(ptext, styles["BodyText"]))
                Story.append(Spacer(1, 0.2 * inch))

    doc.build(Story)
    buffer.seek(0)
    return buffer


st.set_page_config(
    page_title="Elders home Monitoring App",
    page_icon="👨‍⚕️",
    layout="centered",
    initial_sidebar_state="auto"
)

# Initilizing the gemini and graph
if "model_init" not in st.session_state:
    st.session_state.my_gemini = GeminiInitializer()
    st.session_state.my_graph = GraphInitializer()   
    st.session_state.model_init = True

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False


selected = option_menu(
    menu_title=None,
    options=["Home", "Add New Elder", "Note Enhancement", "Plan Generation", "Display"],
    icons=["house", "clipboard-heart-fill", "card-list", "calendar-heart-fill", "person", "database"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    )

if "active_tab" not in st.session_state:
    st.session_state.active_tab = selected

if selected != st.session_state.active_tab:
    if "text_copy" in st.session_state:
        del st.session_state.text_copy
    st.session_state.active_tab = selected

# Home tab
if selected == "Home":
    image_path = 'home_image.jpg' 
    base64_image = get_image_as_base64(image_path)
    background_image_css = f"background-image: url('data:image/png;base64,{base64_image}');"

    description = f"""
    <div style="
        position: relative;
        text-align: justify;
        color: black;
        {background_image_css}
        background-size: cover;
        border-radius: 10px;
        padding: 50px;
        ">
        <div style="
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%;  # Adjust the width as needed
            ">
            <h1 style='text-align: center; color: black'>Elders Home Monitoring App</h1>
            <p style="background-color: rgba(128, 128, 128, 0.6); padding: 20px; border-radius: 10px;">Welcome to our innovative Elders Care Monitoring Application. Where compassion meets technology to elevate the standard of care for our beloved seniors. With a seamless blend of intuitive design and advanced functionality, our platform revolutionizes the way caregivers document and track the well-being of their elderly loved ones. From enhancing care notes to generating personalized care plans, we are dedicated to empowering caregivers with the tools they need to provide exceptional care and ensure the comfort and happiness of every senior under their charge. Join us on a journey of care, compassion, and connectivity as we pave the way for a brighter, more dignified future for our elders.</p>
        </div>
    </div>
    """
    st.markdown(description, unsafe_allow_html=True)
    

elif selected == "Add New Elder":
    st.title("Add New Elder Record")

    add_record_container = st.container(border=True)

    with add_record_container:
        col1, col2 = st.columns(2)

        with col1:
            try:
                default_elder_id = get_next_patient_id(st.session_state.my_graph)
            except:
                default_elder_id = ""

            elder_id = st.text_input("Elder ID", value=default_elder_id, help="Enter the numerical ID")
        
        uploaded_file = st.file_uploader("Choose a txt file", type=['txt'], accept_multiple_files=False)
        
        if uploaded_file:
            bytes_data = ""
            bytes_data = uploaded_file.read()

        col1, col2 = st.columns([4,1])
        
        with col2:
            button = st.button("Submit", type = "primary", use_container_width=True)

    if button: 
        if elder_id == "":
            st.warning("Please enter the Elder ID")
        elif not uploaded_file:
            st.warning("Please upload a text file")
        elif elder_id < default_elder_id:
            st.error(f"Elder id already exists. Please use {default_elder_id} as elder id")
        elif uploaded_file and elder_id != "":
            data = str(bytes_data)
            state = add_patient(st.session_state.my_gemini, st.session_state.my_graph, elder_id, care_note_mode=False, care_note="", data=data)
            if state:
                st.success("Elder added successfully")
            if not state:
                st.error("There was a error while adding the Elder.")
            pass
        

elif selected == "Note Enhancement":
    st.title("Note Enhancement")

    with st.form(key='care_note_form'):
        # col1, col2 = st.columns(2)

        # with col1:
        #     elder_id = st.text_input("Elder ID", value="", help="Enter the numerical ID")
        # with col1:
        #     if not ids_container.empty:
                
        #         elder_id = st.selectbox("Elder ID", ids_container,  key="elder_selectbox")

        #         if elder_id:
        #             elder_details = get_elder_details(elder_id=elder_id)
        #             if isinstance(elder_details, str):
        #                 elder_details = json.loads(elder_details)

        #             if elder_details:
        #                 for key, value in elder_details[0].items():
        #                     if key == 'name':
        #                         st.text_input("Elder Name", value=value)
                
        #         else:
        #             st.warning("Database is empty")
        #             elder_id = st.text_input("Elder ID", value="", help="Enter the numerical ID")
                
            
            
        # with col2:
        #     date = st.date_input("Date")
        #     time = st.time_input("Time")

        # Care note text area outside the columns but still inside the form
        original_care_note = st.text_area("Enter the Care Note:", height=200)

        # Form submit button
        col1, col2 = st.columns([4,1])

        with col2:
            st.session_state.button = st.form_submit_button("Moderate", type = "primary", use_container_width=True)
        
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False
    if 'add_button_shown' not in st.session_state:
        st.session_state.add_button_shown = True

    # Your existing button and condition checks
    # if st.session_state.button and not elder_id:
    #     st.warning("Please enter the Elder ID")
    elif st.session_state.button and not original_care_note:
        st.warning("Please enter the care note to enhance")
    # elif st.session_state.button and elder_id and original_care_note:
    #     st.session_state.enhanced_note, st.session_state.suggestions_note  = note_enhancer(original_care_note, st.session_state.my_gemini)
    #     st.session_state.text_copy = f"""{st.session_state.enhanced_note}"""
    #     st.session_state.text_copy_suggestions = f"""{st.session_state.suggestions_note}"""
    #     st.session_state.button_clicked = True
    elif st.session_state.button and original_care_note:
        st.session_state.enhanced_note, st.session_state.suggestions_note  = note_enhancer(original_care_note, st.session_state.my_gemini)
        st.session_state.text_copy = f"""{st.session_state.enhanced_note}"""
        st.session_state.text_copy_suggestions = f"""{st.session_state.suggestions_note}"""
        st.session_state.button_clicked = True
        
    if "text_copy" in st.session_state and st.session_state.text_copy:
        st.subheader("Generated Care Enhancement Note")
        careNoteDB.insert_data(original_note = original_care_note,care_note=st.session_state.text_copy)
        editable_note = st.text_area(label="",value=st.session_state.text_copy, height=200)
        
        st.subheader("Generated Suggestions")
        st.code("\n".join(tw.wrap(st.session_state.text_copy_suggestions, width=80)), language="md")
        #st.code("\n".join(tw.wrap(st.session_state.text_copy, width=80)), language="md")

        # col1, col2 = st.columns([4,1])
        # if st.session_state.button_clicked:
        #     with col2:
        #         add_button = st.button("Add Care Note", type = "primary", use_container_width=True)
        #     if add_button:
        #         print("Adding the care note")
        #         state = add_patient(st.session_state.my_gemini, st.session_state.my_graph, elder_id, care_note_mode=True, care_note=editable_note, data="")
                
        #         elderDB.insert_data(elder_id=elder_id, original_text=original_care_note, llm_output=st.session_state.text_copy, final_text=editable_note)
                
        #         if state:
        #             st.success("Care Note added successfully")
        #         else:
        #             st.error("There was an error while adding the care note.")
        
elif selected == "Plan Generation":
    st.title("Plan Generation")

    col1, col2 = st.columns(2)

    with col1:
            if not ids_container.empty:
                elder_id = st.selectbox("Elder ID", ids_container)
            else:
                st.warning("Database is empty")
                elder_id = st.text_input("Elder ID", value="", help="Enter the numerical ID")

    with col2:
        st.write("") 
        st.write("")  
        generation_button = st.button("Submit", type="primary")

    if generation_button and elder_id:

        care_plan = generate_plan(elder_id, GeminiInitializer=my_gemini, GraphInitializer=my_graph,
                                  expert_llm=st.session_state.expert_llm,
                                  expert_retriever = st.session_state.mv_retriever)
        st.session_state.care_plan = care_plan  
        carePlanDB.insert_data(elder_id=elder_id, care_plan=care_plan)

    elif not elder_id and generation_button:
        st.warning("Please fill in the elder ID to generate the care plan.")

    if 'care_plan' in st.session_state and st.session_state.care_plan:
        
        st.markdown(st.session_state.care_plan)

        result_pdf = create_pdf("\n".join(tw.wrap(st.session_state.care_plan, width=80)))

        # Download button
        col1, col2 = st.columns([2,1])

        with col2:
            st.download_button(label="Download Care Plan as a PDF",
                            data=result_pdf,
                            file_name=f"care_plan_{elder_id}.pdf",
                            mime='application/pdf',
                            type="primary")
            
elif selected == "Display":
    
    selected_item = st.sidebar.selectbox("Choose an option", ["Elder Details","Care Note DB","Care Plan DB"])

    if selected_item=="Elder Details":
        col1, col2 = st.columns(2)
    
        with col1:
            if not ids_container.empty:
                elder_id = st.selectbox("Elder ID", ids_container)
            else:
                st.warning("Database is empty")
                elder_id = st.text_input("Elder ID", value="", help="Enter the numerical ID")
    
        with col2:
            st.write("") 
            st.write("")  
            generation_button = st.button("Submit", type="secondary")
    
        if generation_button and elder_id:
            
            elder_details = get_elder_details(elder_id=elder_id)
    
            if isinstance(elder_details, str):
                elder_details = json.loads(elder_details)
    
            if elder_details:
                st.markdown("### Elder Information")
                for key, value in elder_details[0].items():
                    st.markdown(f"**{key.replace('_', ' ').title()}**: {value}")
            else:
                st.warning("Elder not found in the database")

    # elif selected_item == "SQL DB":
    #     st.subheader("SQL Operations")

    #     operation = st.selectbox("Select Operation", ["Update", "Read", "Delete"])

    #     if not ids_container.empty:
    #         elder_id = st.selectbox("Elder ID", ids_container)
    #     else:
    #         st.warning("Database is empty")
    #         elder_id = st.text_input("Elder ID", value="", help="Enter the numerical ID")

    #     if operation == "Update":

    #         if 'display_data_button' not in st.session_state:
    #             st.session_state.display_data_button = False
    #         if 'submit_update' not in st.session_state:
    #             st.session_state.submit_update = False

    #         st.subheader("Update selected")
    #         key = st.text_input("Elder Key", value="", help="Check Read Operation to get the key")

    #         if key:
    #             try:
    #                 display_data_button = st.button("Display Data", on_click=lambda: st.session_state.update(display_data_button=True))

    #                 if st.session_state.display_data_button:
    #                     read_data = elderDB.read_data(elder_id=elder_id)
    #                     for record in read_data:
    #                         if str(record[0]) == str(key):
    #                             date_time= st.text_input("Date && Time", value=record[2], help="Enter the date and time", key="date_time")
    #                             user_input_text = st.text_input("User Input Text", value=record[3], help="Enter the user input text", key="user_input_text")
    #                             llm_generated_text = st.text_input("LLM Generated text", value=record[4], help="Enter the LLM generated text", key="llm_generated_text")
    #                             final_text = st.text_input("Final text", value=record[5], help="Enter the final text", key="final_text")

    #                             submit_update = st.button("Update Record", on_click=lambda: st.session_state.update(submit_update=True))

    #                             if st.session_state.submit_update:
    #                                 status = elderDB.update_data(id=record[0], date_time=date_time, elder_id=elder_id, original_text=user_input_text, llm_output=llm_generated_text, final_text=final_text)
    #                                 if status == "done":
    #                                     st.success(f"Record {elder_id} updated successfully")
    #                                     st.session_state.submit_update = False  
    #                                 else:
    #                                     st.warning("Try again")
    #                                     st.session_state.submit_update = False 
    #             except ValueError as e:
    #                 st.error(e)

    #     elif operation == "Read":
    #         st.subheader("Read selected")
    #         read_button = st.button("Read Record")
    #         if read_button:
    #             read_data = elderDB.read_data(elder_id=elder_id)
    #             st.success(f"Displaying record for ID {elder_id}")
    #             for record in read_data:
    #                 formatted_datetime = datetime.strptime(record[2], "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y %I:%M %p")
    #                 st.markdown(
    #                     f"""
    #                     <div style="border:1px solid #e6e6e6; border-radius:10px; padding:15px; margin-bottom:10px;">
    #                         <p><strong>Elder Key:</strong> {record[0]}</p>
    #                         <p><strong>Elder ID:</strong> {record[1]}</p>
    #                         <p><strong>Date time:</strong> {formatted_datetime}</p>
    #                         <p><strong>User Input Text:</strong> {record[3]}</p>
    #                         <p><strong>LLM Generated text:</strong> {record[4]}</p>
    #                         <p><strong>Final text:</strong> {record[5]}</p>
    #                     </div>
    #                     """,
    #                     unsafe_allow_html=True
    #                 )

    #     elif operation == "Delete":
    #         st.subheader("Delete selected")
    #         key = st.text_input("Elder Key", value="", help="Check Read Operation to get the key")

    #         delete_button = st.button("Delete Record")
    #         if delete_button:
    #             read_data = elderDB.delete_data(id=key, elder_id=elder_id)
    #             st.success(f"Record {key} deleted successfully")
                
    elif selected_item == "Care Note DB":
        st.subheader("Care Note DB")

        id = st.text_input("ID", value='all')
        if id == "all":
            id = None
        else:
            id = int(id)
        operation = st.selectbox("Select Operation", ["Read", "Update", "Delete"])

        if operation == "Read":
            st.subheader("Read selected")
            read_button = st.button("Read Record")
            if read_button:
                read_data = careNoteDB.read_data(id)
                if read_data:
                    st.success("Displaying record")
                    for record in read_data:
                        formatted_datetime = datetime.strptime(record[1], "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y %I:%M %p")
                        st.markdown(
                            f"""
                            <div style="border:1px solid #e6e6e6; border-radius:10px; padding:15px; margin-bottom:10px;">
                                <p><strong>ID:</strong> {record[0]}</p>
                                <p><strong>Date time:</strong> {formatted_datetime}</p>
                                <p><strong>Care Note:</strong> {record[2]}</p>
                                <p><strong>Care Note:</strong> {record[3]}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.error("No records found.")

        
        elif operation == "Update":

            if 'display_data_button' not in st.session_state:
                st.session_state.display_data_button = False
            if 'submit_update' not in st.session_state:
                st.session_state.submit_update = False

            st.subheader("Update selected")
            # key = st.text_input("ID", value="", help="Check Read Operation to get the key")
            display_data_button = st.button("Display Data", on_click=lambda: st.session_state.update(display_data_button=True))
            if id and st.session_state.display_data_button:
                try:
                    if id is not None:
                        read_data = careNoteDB.read_data(id=id)
                        if read_data:
                            for record in read_data:
                                if str(record[0]) == str(id):
                                    user_care_note = st.text_area("LLM Generated Note:", value=record[2], help="Enter the care note", key="user_care_note", height=400)
                                    original_care_note = st.text_area("User Input Note:", value=record[2], help="Enter the care note", key="original_care_note", height=400)
                                    submit_update = st.button("Update Record", on_click=lambda: st.session_state.update(submit_update=True))

                                    if st.session_state.submit_update:
                                        status = careNoteDB.update_data(id=record[0],care_note=user_care_note,original_note=original_care_note)
                                        if status == "done":
                                            st.success(f"Record is updated successfully")
                                            st.session_state.submit_update = False  
                                        else:
                                            st.warning("Try again")
                                            st.session_state.submit_update = False 
                        else:
                            st.error("No records found.")
                except ValueError as e:
                    st.error(e)

        
        elif operation == "Delete":
            st.subheader("Delete selected")
            delete_button = st.button("Delete Record")
            if delete_button:
                read_data = careNoteDB.delete_data(id=id)
                st.success(f"Record {id} deleted successfully")

    elif selected_item == "Care Plan DB":
        st.subheader("SQL Operations")

        operation = st.selectbox("Select Operation", ["Read", "Update", "Delete"])

        if not ids_container.empty:
            elder_id = st.selectbox("Elder ID", ids_container)
        else:
            st.warning("Database is empty")
            elder_id = st.text_input("Elder ID", value="", help="Enter the numerical ID")

        if operation == "Read":
            st.subheader("Read selected")
            read_button = st.button("Read Record")
            if read_button:
                read_data = carePlanDB.read_data(elder_id=elder_id)
                if read_data:
                    st.success(f"Displaying record for ID {elder_id}")
                    for record in read_data:
                        formatted_datetime = datetime.strptime(record[2], "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y %I:%M %p")
                        st.markdown(
                            f"""
                            <div style="border:1px solid #e6e6e6; border-radius:10px; padding:15px; margin-bottom:10px;">
                                <p><strong>ID:</strong> {record[0]}</p>
                                <p><strong>Elder ID:</strong> {record[1]}</p>
                                <p><strong>Date time:</strong> {formatted_datetime}</p>
                                <p><strong>Care Plan:</strong> {record[3]}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.error("No records found.")
            
                    
        elif operation == "Update":

            if 'display_data_button' not in st.session_state:
                st.session_state.display_data_button = False
            if 'submit_update' not in st.session_state:
                st.session_state.submit_update = False

            st.subheader("Update selected")
            key = st.text_input("ID", value="", help="Check Read Operation to get the key")

            if key:
                try:
                    display_data_button = st.button("Display Data", on_click=lambda: st.session_state.update(display_data_button=True))

                    if st.session_state.display_data_button:
                        read_data = carePlanDB.read_data(elder_id=elder_id)
                        if read_data:
                            for record in read_data:
                                if str(record[0]) == str(key):
                                    user_care_plan = st.text_area("Care plan", value=record[3], help="Enter the care plan", key="user_care_plan", height=1200)
                                    submit_update = st.button("Update Record", on_click=lambda: st.session_state.update(submit_update=True))

                                    if st.session_state.submit_update:
                                        status = carePlanDB.update_data(id=record[0], elder_id=elder_id, care_plan=user_care_plan)
                                        if status == "done":
                                            st.success(f"Record {elder_id} updated successfully")
                                            st.session_state.submit_update = False  
                                        else:
                                            st.warning("Try again")
                                            st.session_state.submit_update = False 
                        else:
                            st.error("No records found.")
                except ValueError as e:
                    st.error(e)

        

        elif operation == "Delete":
            st.subheader("Delete selected")
            key = st.text_input("ID", value="", help="Check Read Operation to get the key")

            delete_button = st.button("Delete Record")
            if delete_button:
                read_data = carePlanDB.delete_data(id=key, elder_id=elder_id)
                st.success(f"Record {key} deleted successfully")
