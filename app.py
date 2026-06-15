import streamlit as st
from utils.Groq_connection import resume_and_jd_comparison
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
        st.stop()

    if not job_description.strip():
        st.warning("Please enter a job description.")
        st.stop()

    
    try:
        with st.spinner("Analyzing resume and job description..."):
            resume_text = extract_text_from_pdf(uploaded_file)

            result = resume_and_jd_comparison(resume_text, job_description)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()

    if result is None:
        st.error("Analysis failed. Please try again.")
        st.stop()

    st.json(result)