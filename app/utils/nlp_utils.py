from io import BytesIO
from PyPDF2 import PdfReader
import docx2txt
import re

SKILL_KEYWORDS = [
    "python","java","c++","javascript","react","node","flask","django",
    "sql","mongodb","aws","docker","kubernetes","machine learning","nlp","tensorflow","pytorch","pandas","numpy"
]

def extract_text_and_skills(file_bytes: bytes, filename: str):
    text = ""
    ext = filename.lower().split(".")[-1]
    bio = BytesIO(file_bytes)
    try:
        if ext == "pdf":
            reader = PdfReader(bio)
            for p in reader.pages:
                text += p.extract_text() or ""
        elif ext in ("docx", "doc"):
            bio.seek(0)
            text = docx2txt.process(bio)
        else:
            bio.seek(0)
            text = bio.read().decode("utf-8", errors="ignore")
    except Exception:
        text = ""
    cleaned = re.sub(r"\s+", " ", text).strip()
    found = []
    low = cleaned.lower()
    for sk in SKILL_KEYWORDS:
        if sk in low:
            found.append(sk)
    return {"text": cleaned, "skills": list(dict.fromkeys(found))}

def extract_skills_from_text(text: str):
    low = (text or "").lower()
    return [s for s in SKILL_KEYWORDS if s in low]

def extract_skill_words(text: str):
    # simpler token based
    tokens = re.findall(r"\b[a-zA-Z\+\-\.]{2,}\b", (text or "").lower())
    found = [t for t in tokens if t in SKILL_KEYWORDS]
    return list(dict.fromkeys(found))
