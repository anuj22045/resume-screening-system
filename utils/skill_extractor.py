import os


def load_skills() -> list:
    current_dir = os.path.dirname(__file__)
    skills_file = os.path.join(current_dir, "..", "data", "skills.txt")
    skills_file = os.path.normpath(skills_file)

    with open(skills_file, "r", encoding="utf-8") as f:
        skills = [
            skill.strip().lower()
            for skill in f.readlines()
            if skill.strip()
        ]
    return skills


def extract_skills(text: str) -> list:
    text = text.lower()
    skills_db = load_skills()
    found_skills = []

    for skill in skills_db:
        # Match whole-word / phrase to avoid false positives (e.g. "c" in "machine")
        if skill in text:
            found_skills.append(skill)

    return found_skills