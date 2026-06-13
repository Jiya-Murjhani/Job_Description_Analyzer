import streamlit as st
from utils.pdf_parser import extract_text_from_pdf

st.set_page_config(page_title="Job_Description_Analyzer", page_icon="📄")
st.markdown(
    '''<h1 style= "text-align: center; font-size: 3rem; font-weight: bold; background: linear-gradient(45deg, #007bff, #00cc99); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 20px;">Job Description Analyzer</h1>''', unsafe_allow_html=True)

st.markdown('''<p style="text-align:center; font-size: 1rem; color: #555;">Upload your resume in pdf format and job description to know how well you match the job requirements!</p>''', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Resume(PDF)", type=["pdf"], accept_multiple_files=False)

job_description = st.text_area("Enter Job Description", height=250)

if st.button("Analyze"):
    if not uploaded_file:
        st.warning("Please upload a resume in PDF format.")
        st

    if not job_description.strip():
        st.warning("Please enter a job description.")
        st.stop()

    if uploaded_file and job_description.strip():
        with st.spinner("Extracting text from resume..."):
         resume_text = extract_text_from_pdf(uploaded_file)

        st.subheader("Extracted resume text:")
        st.text_area(" ",value = resume_text , height=300)
        st.caption(f"Resume length: " + str(len(resume_text)) + " characters")



