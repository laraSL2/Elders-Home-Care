import streamlit as st
from streamlit_option_menu import option_menu
from care_note_enhancement import note_enhancer
from care_plan_generator import generate_plan
from knowledge_graph import add_patient
from gemini_initializer import GeminiInitializer
from graph_initializer import GraphInitializer
import textwrap as tw
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from io import BytesIO

my_gemini = GeminiInitializer()
my_graph = GraphInitializer()

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
            # Story.append(Spacer(1, 0.2 * inch))

    doc.build(Story)
    buffer.seek(0)
    return buffer


st.set_page_config(
    page_title="Elder's home Monitoring App",
    page_icon="👨‍⚕️",
    layout="centered",
    initial_sidebar_state="auto",
    # menu_items={
    #     'Get Help': 'https://www.google.com',
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

selected =option_menu(
    menu_title= None,
    options=["Home","Add Record","Care Note Enhancement","Care Plan Generation"],
    icons=["house","clipboard-heart-fill","card-list","calendar-heart-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Display content based on selected tab
if selected == "Home":
    # Content for Home 1
        # Custom CSS to style the title
    custom_css = """
    <style>
    body {
        color: black; /* Black text */
    }
    .title {
        font-size: 3rem; /* Adjust the font size as needed */
        text-align: center;
        padding: 20px; /* Add padding for better visibility */
        text-decoration-color: white; /* White underline */
    }
    .subheader {
        font-size: 3rem; /* Adjust the font size as needed */
        text-align: left;
        margin-top: 30px; /* Add some space between title and subheader */
        font-style: italic; /* Italic */
    }
    </style>
    """

    # Display the title with custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown("<h1 class='title'>Elder's Home Monitoring Application</h1>", unsafe_allow_html=True)

    # Display the subheader
    #st.markdown("<p class='subheader'>Providing Assistance to the Elderly</p>", unsafe_allow_html=True)
    #st.markdown("<ul class='subheader'><li>About</li></ul>", unsafe_allow_html=True)

     # Description and picture under About
    #st.write("Welcome to our innovative Elders Care Monitoring Application, where compassion meets technology to elevate the standard of care for our beloved seniors. With a seamless blend of intuitive design and advanced functionality, our platform revolutionizes the way caregivers document and track the well-being of their elderly loved ones. From enhancing care notes to generating personalized care plans, we are dedicated to empowering caregivers with the tools they need to provide exceptional care and ensure the comfort and happiness of every senior under their charge. Join us on a journey of care, compassion, and connectivity as we pave the way for a brighter, more dignified future for our elders.")
    # Description and picture under About
    description = """
    Welcome to our innovative Elders Care Monitoring Application, where compassion meets technology to elevate the standard of care for our beloved seniors. With a seamless blend of intuitive design and advanced functionality, our platform revolutionizes the way caregivers document and track the well-being of their elderly loved ones. From enhancing care notes to generating personalized care plans, we are dedicated to empowering caregivers with the tools they need to provide exceptional care and ensure the comfort and happiness of every senior under their charge. Join us on a journey of care, compassion, and connectivity as we pave the way for a brighter, more dignified future for our elders.
    """
    st.markdown(description)
    
    st.image("home_image.jpg", use_column_width=True)

elif selected == "Add Record":
    # my_gemini = GeminiInitializer()
    # my_graph = GraphInitializer()
    st.title("Add New Elder Record")

    add_record_container = st.container(border=True)

    with add_record_container:
        col1, col2 = st.columns(2)

        with col1:
            elder_id = st.text_input("Elder ID", value="", help="Enter the numerical ID")
        
        uploaded_files = st.file_uploader("Choose a txt file", accept_multiple_files=True)
        
        bytes_data = ""
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            #st.write("filename:", uploaded_file.name)
            #st.write(bytes_data)

        col1, col2 = st.columns([4,1])
        
        with col2:
            button = st.button("Submit", type = "primary", use_container_width=True)

    if button and bytes_data != "" and elder_id != "":
        data = str(bytes_data)
        state = add_patient(my_gemini, my_graph, elder_id, care_note_mode=False, care_note="", data=data)
        if state:
            st.success("Elder added successfully")
        if not state:
            st.error("There was a error while adding the Elder.")
        pass
    
    if button and elder_id == "":
        st.warning("Please enter the Elder ID")
    
    if button and bytes_data == "":
        st.warning("Please upload a text file")


    #pass  # Placeholder
elif selected == "Care Note Enhancement":
    # Content for Home 2
    #st.title("Hello Home 2")
    st.title("Care Note Enhancement")

    container = st.container(border=True)

    with container:
        col1, col2 = st.columns(2)

        with col1:
            elder_id = st.text_input("Elder ID", value="", help="Enter the numerical ID")
        
        with col2:
            date = st.date_input("Date")
            time = st.time_input("Time")
        original_care_note = st.text_area("Enter the Care Note:", height=200) # text input
        
        col1, col2 = st.columns([4,1])
        
        with col2:
            st.session_state.button = st.button("Submit", type = "primary", use_container_width=True)

            # Initialize session state variables if they don't already exist
        if 'button_clicked' not in st.session_state:
            st.session_state.button_clicked = False
        if 'add_button_shown' not in st.session_state:
            st.session_state.add_button_shown = True

        # Your existing button and condition checks
        if st.session_state.button and not elder_id:
            st.warning("Please enter the Elder ID")
        elif st.session_state.button and not original_care_note:
            st.warning("Please enter the care note to enhance")
        elif st.session_state.button and elder_id and original_care_note:
            st.session_state.enhanced_note = note_enhancer(original_care_note, my_gemini)
            
            st.session_state.text_copy = f"""{st.session_state.enhanced_note}"""
            
            st.session_state.button_clicked = True
            
        if "text_copy" in st.session_state and st.session_state.text_copy:
            st.subheader("Generated Care Enhancement Note")
            st.markdown("Copy Care Note Enhancement")
            st.code("\n".join(tw.wrap(st.session_state.text_copy, width=80)), language="md")

        col1, col2 = st.columns([4,1])
        if st.session_state.button_clicked:
            with col2:
                add_button = st.button("Add Care Note", type = "primary", use_container_width=True)
            if add_button:
                print("Adding the care note")
                state = add_patient(my_gemini, my_graph, elder_id, care_note_mode=True, care_note=st.session_state.enhanced_note, data="")
                if state:
                    st.success("Care Note added successfully")
                else:
                    st.error("There was an error while adding the care note.")
        
elif selected == "Care Plan Generation":
    # Content for Home 3
    st.title("Care Plan Generation")

    # Columns for input and button
    col1, col2 = st.columns(2)

    # Input for Elder ID
    with col1:
        elder_id = st.text_input("Elder ID", value="", help="Enter the numerical ID")

    with col2:
        st.write("") 
        st.write("")  
        generation_button = st.button("Submit")

    if generation_button and elder_id:
        # my_gemini = GeminiInitializer()
        # my_graph = GraphInitializer()
        care_plan = generate_plan(elder_id, GeminiInitializer=my_gemini, GraphInitializer=my_graph)
        st.session_state.care_plan = care_plan  
    elif not elder_id and generation_button:
        st.warning("Please fill in the elder ID to generate the care plan.")

    if 'care_plan' in st.session_state and st.session_state.care_plan:
        st.subheader("Generated Care Plan")
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

        
