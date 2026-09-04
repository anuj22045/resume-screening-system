# AI Resume Screening System — Project Documentation

---

## 📌 Unique Points

- Fully AI-powered resume screening using NLP — no manual comparison needed
- Instant skill gap analysis — shows matched, missing, and extracted skills
- Supports both **PDF** and **DOCX** resume formats
- Multi-resume ranking — upload multiple resumes and rank them against one job description
- Composite scoring system — combines similarity score (60%) + skill match (40%)
- Experience auto-detection — extracts years of experience from resume text using regex
- Uses a custom skills database (`data/skills.txt`) — easy to expand with new skills
- Beautiful glassmorphism UI built with Streamlit + custom CSS
- Works locally and can be deployed to cloud (Render, etc.)

---

## 🔄 Workflow

1. **User uploads a resume** (PDF or DOCX) and **pastes a job description**
2. **Text extraction** — resume file is parsed and raw text is extracted
3. **Preprocessing** — text is cleaned (lowercase, remove special chars, remove emails, remove numbers)
4. **Stopword removal** — common English words like "the", "is", "and" are removed
5. **Lemmatization** — words are reduced to their base form (e.g., "running" → "run")
6. **Skill extraction** — cleaned text is matched against a predefined skills database
7. **Similarity calculation** — TF-IDF vectors are created for resume skills and JD skills, then cosine similarity is calculated
8. **Scoring** — resume score, skill match %, and experience years are computed
9. **Results displayed** — metric cards, progress bars, skill tags, and recommendation banner are shown

---

## 🧠 Role of NLP in This Project

- **Text Preprocessing** — NLP techniques clean raw resume/JD text for accurate comparison
- **Tokenization** — splits text into individual words for analysis
- **Stopword Removal** — NLTK's stopword list removes noise words that don't carry meaning
- **Lemmatization** — NLTK's WordNet Lemmatizer normalizes words to root form for better matching
- **TF-IDF Vectorization** — converts text into numerical vectors based on word importance (Term Frequency × Inverse Document Frequency)
- **Cosine Similarity** — measures how close the resume and job description are in vector space (0 = no match, 1 = perfect match)
- **Keyword Matching** — extracted skills are compared between resume and JD to find gaps

---

## 🛠️ Tech Stack

- **Python** — core language
- **Streamlit** — web UI framework
- **NLTK** — NLP library (stopwords, lemmatization, wordnet)
- **scikit-learn** — TF-IDF vectorizer + cosine similarity
- **pdfplumber** — PDF text extraction
- **python-docx** — DOCX text extraction

---

## 📁 Project Structure

```
Resume-screening-system/
├── app.py                  → Main Streamlit application
├── style.css               → Custom UI styling
├── requirements.txt        → Python dependencies
├── download_nltk.py        → Script to download NLTK data
├── data/
│   └── skills.txt          → Skills database (one skill per line)
├── utils/
│   ├── pdf_reader.py       → PDF & DOCX text extraction
│   ├── preprocess.py       → Text cleaning & NLP preprocessing
│   ├── similarity.py       → TF-IDF + cosine similarity
│   ├── skill_extractor.py  → Skill matching from text
│   └── experience.py       → Experience years extraction
└── nltk_data/              → Local NLTK resources (stopwords, wordnet, punkt)
```
