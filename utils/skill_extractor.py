import os

def load_skills():
    current_dir = os.path.dirname(__file__)

    skills_file = os.path.join(
        current_dir, "..","data", "skills.txt"
    )

    with open(skills_file, "r", encoding="utf-8") as f:
        skills=[
            skill.strip().lower()
            for skill in f.readlines()
        ]
    return skills

def extract_skills(text):
    text = text.lower()

    skills_db = load_skills()
    found_skills=[]

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    return found_skills

print("skill_extractor loaded successfully")