from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text: str, jd_text: str) -> float:
    """
    Calculate cosine similarity between resume and job description text
    using TF-IDF vectors. Returns 0.0 if either input is empty.
    """
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    documents = [resume_text, jd_text]
    vectorizer = TfidfVectorizer()

    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return float(similarity_score[0][0])
    except ValueError:
        # Raised when vocabulary is empty after preprocessing
        return 0.0
