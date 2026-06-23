import streamlit as st
from utils.pdf_reader import extract_text_from_pdf

from utils.preprocess import preprocess_text

from utils.similarity import calculate_similarity

from utils.experience import extract_experience


st.set_page_config(
    page_title="Resume Screening System",
    page_icon="📄",
    layout="wide"
)

from utils.skill_extractor import extract_skills#####

# print(extract_skills)

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
        experience = extract_experience(resume_text)
        clean_resume_text = preprocess_text(resume_text)

        # st.subheader("Preprocessed Resume Text")
        # st.text_area("Clean Resume Text", clean_resume_text, height=300)

        #######------Extracting skills from resume using skill_extractor.py --------------#######
        resume_skills = extract_skills(clean_resume_text)
        
        #######################################################################################

        # clean_job_description = preprocess_text(job_description)
        # similarity_score = calculate_similarity(clean_resume_text, clean_job_description)
        clean_job_description = preprocess_text(job_description)

        resume_skills = extract_skills(clean_resume_text)

        jd_skills = extract_skills(clean_job_description)
        missing_skills = list(set(jd_skills) - set(resume_skills))
        matching_skills = list(set(resume_skills) & set(jd_skills))
        if len(jd_skills) > 0:
            skill_match_percentage = round(
                (len(matching_skills) / len(jd_skills)) * 100,2
                )
        else:
            skill_match_percentage = 0
        ##for testing purpose
        # st.write("Resume Skills:", resume_skills)
        # st.write("JD Skills:", jd_skills)
        # st.write("Missing Skills:", missing_skills)

        resume_skill_text = " ".join(resume_skills)

        jd_skill_text = " ".join(jd_skills)

        similarity_score = calculate_similarity(
            resume_skill_text,
            jd_skill_text)
        
        resume_score = round(similarity_score *100, 2)
        ##analysis Results
        st.subheader("Analysis Results")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Resume score", f"{resume_score}%")
        with col2:
            st.metric("Skill Match", f"{skill_match_percentage}%")
            
        col3, col4 = st.columns(2)
        with col3:
            if len(missing_skills) >0:
                st.metric("Missing Skills", len(missing_skills))
            else:
                st.metric("No missing Skills found", "All Skills matched")

        with col4:
            if experience > 0:
                st.metric("Experience ", f"{experience} Years")
            else:
                st.metric("Experience", "Not Found")


        st.subheader("Extracted Skills")
        for skill in resume_skills:
            st.write(f"✅ {skill.title()}")

        st.subheader("Missing Skills")  
        for skill in missing_skills:
            st.write(f"❌ {skill.title()}")

        st.subheader("Matching Skills")
        for skill in matching_skills:
            st.write(f"✅ {skill.title()}")
        
        st.subheader("Recommendations")
        if (skill_match_percentage >= 90 and resume_score >= 50 and len(missing_skills)<=2):
            st.success("Resume is suitable for this role.")
        elif (skill_match_percentage >= 70 and resume_score >=50 and len(missing_skills)<= 4):
            st.warning(f"Good Match, but consider improving your skills in {' '.join(missing_skills)}")

        else:
            st.error(f"Not a strong match. Focus on learning: {', '.join(missing_skills)}")
        
        

elif not uploaded_file:
        st.error("Please upload a resume")

elif not job_description:
        st.error("Please enter a job description")

# st.progress(int(resume_score))