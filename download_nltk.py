"""
Download required NLTK resources into the project-local nltk_data directory.
Run once with:  python download_nltk.py
"""
import os
import nltk

# Download into the project-local nltk_data folder (cross-platform)
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "nltk_data")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

resources = [
    "punkt",
    "punkt_tab",
    "stopwords",
    "wordnet",
    "omw-1.4",
]

for resource in resources:
    print(f"Downloading {resource}...")
    nltk.download(resource, download_dir=DOWNLOAD_DIR)

print(f"\nNLTK data downloaded successfully to: {DOWNLOAD_DIR}")