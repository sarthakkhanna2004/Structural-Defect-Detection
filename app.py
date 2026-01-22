import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt
import os

#configure the model
gemini_api_key= os.getenv('Google_api_key1')
genai.configure(api_key=gemini_api_key)
model= genai.GenerativeModel('gemini-2.5-flash')

# Let's create sidebar for image upload

st.sidebar.title(":red[Upload the image of defect]")
uploaded_image = st.sidebar.file_uploader('Choose an images file', type=['png', 'jpg', 'jpeg', 'jfif'],
                                          accept_multiple_files=True)

uploaded_image= [Image.open(img) for img in uploaded_image]
if uploaded_image:
    st.sidebar.success('Images have been uploaded successfully!')
    st.sidebar.subheader(':blue[Uploaded Images]')
    st.sidebar.image(uploaded_image)

#Lets create the main page
st.title(':orange[STRUCTURAL DEFECT:-]  :violet[AI Assisted Structural Defect Identifier]')
st.markdown('#### :green[This application takes the images of structural defects from construction site and prepares the AI assisted report.]')
title= st.text_input('Enter the title of the report:')
name= st.text_input('Enter the name of the person who has prepared the report:')
designation=  st.text_input('Enter the designation of the person who has prepared the report:')
organization= st.text_input('Enter the name of the organization:')

if st.button('Submit'):
    with st.spinner('Processing...'):
        prompt= f'''
        <Role> You are an expert engineer with 20+ year sof experience in the construction industry.
        <Goal> You need to prepare a detailed report on the structural defect shown in the images provided by the user.
        <Context> The images shared by the use have been attached.
        <Format> Follow the steps to prepare the report
        * add title at the top of the report. The title provided by the user is {title}.
        * next add name, designation and organization of a person who has prepared the report. Also include the date. Folowing are the details provided by the user
        name:{name}, 
        designation={designation}, 
        organization={organization}
        date : {dt.datetime.now().date()}
        * Identify and classify the defect. for eg: crack, spalling, corossion, honeycombing, etc.
        * There could be more than 1 defect in the images. Identify all defects separately.
        * For each defect identified, provide a short description of the defect and its potential impact on the structure.
        * For each defect measure the severity as low, medium or high. Also mentioning, if the defect is inevitable or avoidable.   
        * Provide the short terma nd long term solution for the repair along with an estimated cost in INR and estimated time of repair.
        * What precautionary measures can be taken to avoid these defects in future.
        

        <Instructions>
        * The report generated should be in word format.
        * Use bullet points and tabular format wherever possible.
        *  Do not use HTML formats like <br> and others
        * Make sure the report doesn't exceed three pages.
        '''

        response= model.generate_content([prompt, *uploaded_image], generation_config={'temperature':0.9})
        st.write(response.text)

    if st.download_button(
        label= 'Click to download', 
        data= response.text,
        file_name= 'structural_defect_report.txt',
        mime='text/plain'):
        st.success('Your file is downloaded.')