import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
st.set_page_config(
    page_title="Resume Screening System",
    page_icon="📄",
    layout="wide"
)

st.title("AI Resume Screening System")
st.write("Upload a Resume and compare it with a job using NLP")

st.subheader("Upload Resume")

uploaded_file = st.file_uploader("choose Resume", type=["pdf", "docx"])

if uploaded_file:
    st.write("Resume uploaded successfully")


st.subheader("Job Description")

job_description = st.text_area("Enter job description here", height=200)

analyze = st.button("Analyze Resume")

if analyze:
    if uploaded_file and job_description:
        st.write("Analyzing the resume against the job description..")
        resume_text = extract_text_from_pdf(uploaded_file)
        st.subheader("Extracted Resume Text")
        st.text_area("Resume Text", resume_text, height=300)

##analysis Results
    st.subheader("Analysis Results")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Resume score", "85%")

    with col2:
        st.metric("Skill Found", 12)

    col3, col4 = st.columns(2)

    with col3:
        st.metric("Missing Skills", 3)

    with col4:
        st.metric("Experience ", "2 years")
        
elif not uploaded_file:
        st.error("Please upload a resume")

elif not job_description:
        st.error("Please enter a job description")

st.subheader("Extracted skills")

skills =["Python", "Machine learning", "Data analysis", "NLP", "Deep Learning"]

for skill in skills:
    st.write(f"✅ {skill}")

st.subheader("Missing Skills")
missing_skills = ["Cloud computing", "Docker", "Kubernetes"]

for skill in missing_skills:
    st.write(f"❌ {skill}")


st.subheader("Recommendation")

st.success(
    "Resume is suitable for this role."
)