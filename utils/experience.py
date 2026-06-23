import re

def extract_experience(text):
    patterns=[
        r'(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?',
    ]
    experience=0
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        for match in matches:
            experience = max(experience, int(match))
    
    return experience