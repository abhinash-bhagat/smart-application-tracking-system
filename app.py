import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()  # Load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return json.loads(response.text)  # Assuming the response is a JSON string

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt_template = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst,
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and
the missing keywords with high accuracy.
resume: {text}
description: {jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
"""

# Streamlit app
st.set_page_config(layout="wide",page_icon="📄",page_title="Smart ATS")
st.title("Smart ATS")
jd = st.text_area("Paste the Job Description")
uploaded_files = st.file_uploader("Upload Your Resumes", type="pdf", help="Please upload the PDFs", accept_multiple_files=True)

if uploaded_files:
    num_documents = len(uploaded_files)
    num_top_applicants = st.slider("Select number of top applicants to display", min_value=1, max_value=num_documents, value=min(5, num_documents))
    
    submit = st.button("Submit")

    if submit:
        if uploaded_files:
            evaluations = []
            for uploaded_file in uploaded_files:
                text = input_pdf_text(uploaded_file)
                input_prompt = input_prompt_template.format(text=text, jd=jd)
                response = get_gemini_response(input_prompt)
                evaluations.append({"file_name": uploaded_file.name, "evaluation": response})

            # Sort evaluations by JD Match percentage in descending order
            evaluations.sort(key=lambda x: float(x['evaluation']['JD Match'].strip('%')), reverse=True)

            # Get top N resumes based on user selection
            top_evaluations = evaluations[:num_top_applicants]

            # Display stacked format
            for eval in top_evaluations:
                st.header(eval['file_name'])
                st.write(f"**JD Match**: {eval['evaluation']['JD Match']}")
                st.write(f"**Missing Keywords**: {', '.join(eval['evaluation']['MissingKeywords'])}")
                st.write(f"**Profile Summary**: {eval['evaluation']['Profile Summary']}")
                st.markdown("---")  # Add a horizontal line for separation
        else:
            st.write("Please upload at least one PDF file.")
else:
    st.write("Please upload at least one PDF file.")
