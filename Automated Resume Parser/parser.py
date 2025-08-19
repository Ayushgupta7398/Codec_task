import pdfplumber
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

def extract_info(text):
    doc = nlp(text)
    name = ""
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.search(r'(\+?\d[\d\s\-\(\)]{8,}\d)', text)

    skill_keywords = ['Python', 'Java', 'C++', 'Flask', 'React', 'SQL', 'Machine Learning']
    skills = [s for s in skill_keywords if s.lower() in text.lower()]

    education_keywords = ['B.Tech', 'M.Tech', 'B.Sc', 'M.Sc', 'Bachelor', 'Master', 'PhD']
    education = [line.strip() for line in text.split("\n") if any(kw in line for kw in education_keywords)]

    return {
        "name": name,
        "email": email.group(0) if email else "",
        "phone": phone.group(0) if phone else "",
        "skills": ", ".join(skills),
        "education": " | ".join(education)
    }
