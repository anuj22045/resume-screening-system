import re
import os
import nltk

# Add project-local nltk_data directory first, then fall back to system paths
_LOCAL_NLTK_DIR = os.path.join(os.path.dirname(__file__), "..", "nltk_data")
_LOCAL_NLTK_DIR = os.path.normpath(_LOCAL_NLTK_DIR)

if _LOCAL_NLTK_DIR not in nltk.data.path:
    nltk.data.path.insert(0, _LOCAL_NLTK_DIR)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def preprocess_text(text: str) -> str:
    text = text.lower()

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Remove standalone numbers
    text = re.sub(r"\b\d+\b", "", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", "", text)

    # Tokenize by whitespace (avoids punkt dependency)
    words = text.split()

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]

    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    return " ".join(words)
