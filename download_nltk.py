import os
import nltk

DOWNLOAD_DIR = "/opt/render/nltk_data"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

resources = [
    "punkt",
    "punkt_tab",
    "stopwords",
    "wordnet",
    "omw-1.4"
]

for resource in resources:
    print(f"Downloading {resource}...")
    nltk.download(resource, download_dir=DOWNLOAD_DIR)

print("NLTK data downloaded successfully!")