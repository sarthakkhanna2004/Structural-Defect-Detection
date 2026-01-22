import streamlit as st

import google.generativeai as genai
from PIL import Image
import datetime as dt
import os

# Configure the model
gemini_api_key = os.getenv('Google_api_key1')
genai.configure(api_key = gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

if "report_text" not in st.session_state:
    st.session_state.report_text = None

# Let's create the sidebar for image upload
st.sidebar.title('Upload the image here.')
uploaded_image = st.sidebar.file_uploader('Image', type = ['jpeg', 'jpg', 'png', 'jfif'],
                                          accept_multiple_files= True)

images = []

if uploaded_image:
    st.sidebar.success('Images have been uploaded successfully')
    st.sidebar.subheader('Uploaded Images')
    st.sidebar.image(uploaded_image)

    # Convert uploaded files to PIL Images
    for img in uploaded_image:
        images.append(Image.open(img))

# Let's create the main page
st.markdown(
    """
    <h1 style="
        font-size:52px;
        font-weight:700;
        display:inline-block;
    ">
        <span style="color:#215E61;">STRUCTURAL DEFECT:</span>
        <span style="color:#FF8C2A;"> Structural Defect Identifier</span>
    </h1>
    """,
    unsafe_allow_html=True
)
st.markdown('#### This application takes the images of structural defects from' \
' the construction site and prepares an AI assisted report.')
title = st.text_input('Enter the title of the report:')
name = st.text_input('Enter the name of the person who has prepared the report:')
desig = st.text_input('Enter the designation of the person who has prepared the report:')
orgz = st.text_input('Enter the name of the organization:')

st.markdown("---")

if st.button('Generate Inspection Report'):
    if not images:
        st.warning("Please upload at least one image.")
        st.stop()

    with st.spinner('Analyzing defects and generating report...'):
        prompt = f'''
        <Role> You are an expert structural engineer with 20+ years experience in the construction
        industry. 
        <Goal> You need to prepare a detailed report on the structural defect shown in the images 
        provided by the user. 
        <Context> The images shared by the user have been attached. 
        <Format> Follow the stes to prepare the report:
        * Add title at the top of the report. The title provided by the user is {title}.
        * Next add name, designation and organisation of the person who has prepared the report. 
        Also include the date. Following are the details provided by the user -
        name: {name}
        designation: {desig}
        organization: {orgz}
        date: {dt.datetime.now().date()}
        * Identify and classify the defect for eg: crack, spalling, corossion, honeycombing etc.
        * There could be more than one defects in images. Identify all defects separately.  
        * For each defect identified, provide a short description of the defect and its potential
        impact on the structure. 
        * For each defect measure the severity as low, medium or high. Also mentioning if the defect is
        inevitable or avoidable.  
        * Provide the short-term and long-term solution for the repair along with an estimated 
        cost in INR and estimated time.
        * What precautionary measures can be taken to avoid these defects in future. 

        <Instructions>
        * Do not include HTML formats like <br> and others.
        * The report generated should be in word format.
        * Use bullet points and tables where ever possible.
        * Make sure the report does not exceed 3 pages.  
        '''
        response = model.generate_content([prompt, *images],
                                          generation_config={'temperature': 0.9})
        
        st.session_state.report_text = response.text.replace("<br>", "\n")


if st.session_state.report_text:
    st.success("Report generated successfully")
    st.markdown("## Generated Inspection Report")
    st.markdown(st.session_state.report_text)

    st.download_button(
        label="Download Report",
        data=st.session_state.report_text,
        file_name="structural_defect_report.txt",
        mime="text/plain"
    )