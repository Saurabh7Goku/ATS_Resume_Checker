from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import io
import pdf2image
import base64
import google.generativeai as genai


load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def response(input, pdf, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        # Take the first page for simplicity, or loop through images for all pages
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="Resume Checker", layout='wide')
header_style = """
    <style>
        .header {
            text-align: center;
            # padding: -20em;
            margin: -2em;
        }
    </style>
"""

# Display the custom style
st.markdown(header_style, unsafe_allow_html=True)
st.markdown("<h1 class='header'>ATS Resume Checker System</h1>", unsafe_allow_html=True)
st.divider()
# Create two columns
col1, col2 = st.columns(2)

# Text area in the first column
input_text = col1.text_area("Company's Job Description", key="input", height=250)

# File uploader in the second column
uploaded_file = col2.file_uploader("PDF Resume Here...", type=['pdf'])
pdf_content = ""

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

col1, col2, col3, col4, col5, col6 = st.columns(6)


submit1 = col2.button("Tell Me About the Resume")

submit2 = col3.button("Improvise my Resume")

submit3 = col4.button("Missing Keywords")

submit4 = col5.button("Percentage match")

c1, c2, c3 = st.columns(3)
sus = c2.button('Improve Experience content writing...')

# special_prompt = """
#  You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description.
#  please Check all the spelling mistakes and suggest more impactful way to write Candidate's experience and using action verbs and more impactful,
#  way to write project descriptions.
# """

special_prompt = """
 You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
 Please edit and write down candidate's experience and make it more impact full.
 .
"""


input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an Technical Human Resource Manager with expertise in data science, 
your role is to scrutinize the resume in light of the job description provided. 
Share your insights on the candidate's suitability for the role from an HR perspective. 
Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. As a Human Resource manager,
 assess the compatibility of the resume with the role. Give me what are the keywords that are missing
 Also, provide recommendations for enhancing the candidate's skills and identify which areas require further development.
"""
input_prompt4 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if sus:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        
        response = response(
            input = input_text, 
            pdf = pdf_content,
            prompt = special_prompt
        )
        
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = response(input_prompt1, pdf_content, input_text)

        with st.container():
            st.subheader("The Response is")
            st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")




elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = response(input_prompt4, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")


st.markdown("---")
st.caption("This is just a beta release...")