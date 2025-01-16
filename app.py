from  dotenv  import  load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GENAI_API_KEY'))


def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):

    if uploaded_file is not None:

        ##Coverting the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        ##Converting the image to byte array
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode to base64

            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## Streamlit App

st.set_page_config(page_title="ATS Resume Expert", page_icon="🔮", layout="wide")
st.header("ATS Tracking System")
input_text = st.text_area("Enter Job Description: ",key="input", height=200) 
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about my Resume")
submit2 = st.button("How can I improve my Resume")
submit3 = st.button("Percentage Match with Job Description")

input_prompt1 = """
"You are an experienced HR professional with expertise in reviewing resumes across various tech roles, including Data Science, Machine Learning, Full Stack Web Development, Product Management, Big Data Engineering, DevOps, and Data Analyst. 
Analyze the provided resume and share your insights on the candidate's profile from a hiring manager's perspective.
Based on your expertise, provide a comprehensive evaluation of the candidate's profile. 
* Highlight the candidate's key strengths and areas of expertise. 
* Identify any potential weaknesses or areas for improvement. 
* Offer constructive feedback on how the candidate can enhance their resume for future job applications.
* Provide an overall assessment of the candidate's suitability for a role in the tech industry."
"""

input_prompt2 = """
You are a Technical Human Resources Manager with expertise in reviewing resumes for including Data Science, Machine Learning, Full Stack Web Development, Product Management, Big Data Engineering, DevOps, and Data Analyst positions. 
Your role is to scrutinize the provided resume against the job descriptions for these roles and provide feedback to the candidate on how they can improve their resume to increase their chances of securing a job interview.
From an HR perspective, share your insights on how the candidate can improve their resume to:
* **Better align with the expectations of hiring managers for [**Specific Role**] roles.**
* **Increase the chances of their resume passing through Applicant Tracking Systems (ATS).**
* **Make their resume more appealing and stand out from the competition.**
Offer specific and actionable advice on how the candidate can enhance their resume, such as:
* **Highlighting specific skills and achievements.**
* **Quantifying their accomplishments with data and metrics.**
* **Improving the clarity and conciseness of their resume.**
* **Using strong keywords and action verbs.**
* **Tailoring the resume to specific job descriptions.**

Provide constructive feedback that will help the candidate present their qualifications more effectively to potential employers.
"""

input_prompt3 = """
You are a skilled ATS (Applicatn Tracking System) scanner with a deep understanding of any one job role from Data Science, Machine Learning, Full Stack Web Development, Product Management, Big Data Engineering, DEVOPS, Data Analyst and deep ATS functionality.
Your task is to evaluate the resume agaisnt the provided job description.
Give me the percentage match of the resume with the job description.
First outpput the percentage ans then keywords missing in the resume and your final thoughts.
"""

if submit1:
    try:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("Response : ")
        st.write(response)
    except FileNotFoundError:
        st.write("Please upload a file")
    
elif submit2:
    try:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("Response : ")
        st.write(response)
    except FileNotFoundError:
        st.write("Please upload a file")

elif submit3:
    try:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("Response : ")
        st.write(response)
    except FileNotFoundError:
        st.write("Please upload a file")