import streamlit as st
from utils.Groq_connection import resume_and_jd_comparison
from utils.pdf_parser import extract_text_from_pdf

st.set_page_config(page_title="Job_Description_Analyzer", page_icon="📄")
st.markdown(
    '''<h1 style= "text-align: center; font-size: 3rem; font-weight: bold; background: linear-gradient(45deg, #007bff, #00cc99); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 20px;">Job Description Analyzer</h1>''', unsafe_allow_html=True)

st.markdown('''<p style="text-align:center; font-size: 1rem; color: #555;">Upload your resume in pdf format and job description to know how well you match the job requirements!</p>''', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Resume(PDF)", type=["pdf"], accept_multiple_files=False)

job_description = st.text_area("Enter Job Description", height=250)

if st.button("Analyze" , use_container_width=True):
    if not uploaded_file:
        st.warning("Please upload a resume in PDF format.")
        st.stop()

    if not job_description.strip():
        st.warning("Please enter a job description.")
        st.stop()

    if len(job_description.strip()) < 100:
        st.warning("Your job description seems too short. Results may be inaccurate.")

    try:
        with st.spinner("Analyzing resume and job description..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            if not resume_text.strip():
                st.error("Could not extract text from your PDF. Try a different PDF file.")
                st.stop()
            result = resume_and_jd_comparison(resume_text, job_description)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()

    if result is None:
        st.error("Analysis failed. Please try again.")
        st.stop()
    st.divider()
    st.markdown("## 📄 Analysis Results")
    #------------ Display Match Score and Summary -------------
    st.divider()
    st.markdown("### 📊 Match Score")
    score = result["Match_score"]
    summary = result["Match_summary"]

    st.metric(label="Overall Match", value=f"{score}%")
    st.progress(score / 100)
    st.caption(summary)

    #------------ Display Required Skills -------------
    st.divider()
    st.markdown("### 🎯 Required Skills")

    cols = st.columns(3)

    for i, skill in enumerate(result["Required_skills"]):
        cols[i % 3].markdown(f"• {skill}")

    #------------ Display Matched Skills -------------
    st.divider()
    st.markdown("### ✅ Skills You Have")

    if result["Matched_skills"]:
        for item in result["Matched_skills"]:
            skill = item["skill"]
            confidence = item["confidence"]

            if confidence == "strong":
                st.success(f"✅ {skill} — Strong Match")
            elif confidence == "partial":
                st.warning(f"🟡 {skill} — Partial Match")
    else:
        st.info("No matching skills found.")
#------------ Display Missing Skills-------------
    st.divider()
    st.markdown("### ❌ Skills You're Missing")

    if result["Missing_skills"]:
        for skill in result["Missing_skills"]:
            st.error(f"✗ {skill}")
    else:
        st.success("🎉 You match all required skills — great fit!")
    #------------ Display Suggestions for Missing Skills -------------
    st.divider()
    st.markdown("### 💡 How to Fix Each Gap")

    if result["Suggestions"]:
        for skill, suggestion in result["Suggestions"].items():
            with st.expander(f"How to demonstrate {skill}"):
                st.write(suggestion)
    else:
        st.success("🎉 No gaps to fix! You're a strong match.")
# -------------OVERALL TIP -------------------------------------------
    st.divider()
    st.markdown("### 🧠 Expert Recommendation")

    overall_tip = result.get("Overall_tip", None)

    if overall_tip:
        st.info(f"💬 {overall_tip}")
    else:
        st.info("No additional recommendation available.")