🚀 AI Resume Screening & Candidate Ranking System

An AI-powered Resume Screening System that intelligently evaluates resumes against a Job Description (JD), identifies skill gaps, and ranks multiple candidates using NLP techniques.


📌 Overview

The AI Resume Screening & Candidate Ranking System automates the resume screening process by comparing resumes with a Job Description (JD).

Instead of manually reviewing resumes, recruiters can upload one or multiple resumes and instantly receive:

📄 Resume Match Score
🎯 Skill Match Percentage
✅ Matching Skills
❌ Missing Skills
💼 Experience Detection
🏆 Candidate Ranking
💡 Intelligent Recommendations
✨ Features
📄 Resume Analysis
Upload PDF resumes
Extract resume text automatically
Resume-to-JD similarity analysis
🤖 NLP Processing
Text preprocessing
Stopword removal
Text normalization
TF-IDF Vectorization
Cosine Similarity
🎯 Skill Analysis
Skill extraction
Matching skills
Missing skills
Skill match percentage
💼 Experience Detection
Automatically extracts years of experience from resumes.
🏆 Candidate Ranking
Upload multiple resumes
Automatic candidate ranking
Overall suitability score
Recruiter-friendly dashboard
💡 Recommendation Engine

Provides intelligent recommendations such as:

✅ Suitable for the role
⚠️ Good Match
❌ Not a Strong Match
🛠️ Tech Stack
Category	Technologies
Programming	Python
Frontend	Streamlit
Machine Learning	Scikit-learn
NLP	TF-IDF, Cosine Similarity
Data Processing	Pandas, NumPy
PDF Processing	pdfplumber
Visualization	Matplotlib, Seaborn
📂 Project Structure
Resume-Screeing-System/
│
├── app.py
├── requirements.txt
│
├── utils/
│   ├── pdf_reader.py
│   ├── preprocess.py
│   ├── similarity.py
│   ├── skill_extractor.py
│   └── experience.py
│
└── data/
    └── skills.txt
⚙️ Workflow
Upload Resume(s)
        │
        ▼
Extract Resume Text
        │
        ▼
Preprocess Text
        │
        ▼
Extract Skills
        │
        ▼
Compare with Job Description
        │
        ▼
TF-IDF + Cosine Similarity
        │
        ▼
Calculate Resume Score
        │
        ▼
Detect Experience
        │
        ▼
Generate Recommendation
        │
        ▼
Rank Candidates
📊 Candidate Evaluation Metrics

The system evaluates each resume based on:

Resume Similarity Score
Skill Match Percentage
Matching Skills
Missing Skills
Experience
Overall Candidate Score
