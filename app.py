from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import PyPDF2 as pdf
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

## Groq Response
def get_groq_response(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

## PDF Text Extraction
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += str(reader.pages[page].extract_text())
    return text

## Prompt Templates
input_prompt1 = """
You are an experienced HR with Tech Experience in the field of Data Science, Artificial Intelligence, Machine Learning, Gen AI, Full Stack,
Web Development, Big Data Engineering, DevOps, Data Analyst.
Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
resume: {text}
job description: {jd}
"""

input_prompt2 = """
You are a Technical Human Resource Manager with expertise in Data Science, Artificial Intelligence, Machine Learning, Gen AI, Full Stack,
Web Development, Big Data Engineering, DevOps, Data Analyst.
Your role is to scrutinize the resume in light of the job description provided.
Share your insights on the candidate's suitability for the role from an HR perspective.
Additionally, offer advice on enhancing the candidate's skills and identify areas of improvement.
resume: {text}
job description: {jd}
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Artificial Intelligence, Machine Learning,
Gen AI, Full Stack, Web Development, Big Data Engineering, DevOps, Data Analyst and deep ATS functionality.
Your task is to evaluate the resume against the provided job description.
Give me the percentage of match, keywords missing, and final thoughts.
I want the response in this structure:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
resume: {text}
job description: {jd}
"""

## Streamlit App
st.set_page_config(page_title="HireReady AI")
st.header("HireReady AI 🚀")
st.text("Your Smart Job Application Assistant")

jd = st.text_area("Paste the Job Description", key="input")
uploaded_file = st.file_uploader("Upload Your Resume in PDF Format", type=["pdf"])

if uploaded_file is not None:
    st.write("✅ PDF Uploaded Successfully")

submit1 = st.button("Tell me about the Resume")
submit2 = st.button("How can I Improve my Skills")
submit3 = st.button("Percentage Match")

if submit1:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_groq_response(input_prompt1.format(text=text, jd=jd))
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload your Resume")

elif submit2:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_groq_response(input_prompt2.format(text=text, jd=jd))
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload your Resume")

elif submit3:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_groq_response(input_prompt3.format(text=text, jd=jd))
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload your Resume")