import nltk

resources = [
    "punkt",
    "punkt_tab",
    "stopwords",
    "wordnet",
    "omw-1.4"
]

for resource in resources:
    print(f"Downloading {resource}...")
    nltk.download(resource)