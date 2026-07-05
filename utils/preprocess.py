import re
import nltk

# Tell NLTK where Render stores downloaded data
nltk.data.path.append("/opt/render/nltk_data")

print("NLTK PATHS:", nltk.data.path)

try:
    print("WORDNET LOCATION:", nltk.data.find("corpora/wordnet"))
except Exception as e:
    print("WORDNET ERROR:", e)

# Check that the required datasets are available
for resource in ["stopwords", "wordnet", "omw-1.4"]:
    try:
        nltk.data.find(f"corpora/{resource}")
    except LookupError:
        nltk.download(resource, download_dir="/opt/render/nltk_data")

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def preprocess_text(text):
    text  =text.lower()

    #remove special character
    text  = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    text = re.sub(r"\d+", "", text)

    text = re.sub(r'\S*@\S*\s?', '', text)

    text = re.sub(r'\S+@\S+', '', text)

    #tokenization
    # words = word_tokenize(text)
    words = text.split()

    #remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]

    #lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    cleaned_text = " ".join(words)

    return cleaned_text
