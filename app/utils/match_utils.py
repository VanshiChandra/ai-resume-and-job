from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def normalize_text(t: str):
    return re.sub(r"[^a-z0-9\s]", " ", (t or "").lower())

def match_resume_to_job_text(resume_text: str, job_text: str):
    r = normalize_text(resume_text)
    j = normalize_text(job_text)
    sim = 0.0
    try:
        vec = TfidfVectorizer(stop_words="english")
        X = vec.fit_transform([r, j])
        sim = float(cosine_similarity(X[0:1], X[1:2])[0][0])
    except Exception:
        sim = 0.0
    matched = list(set(r.split()) & set(j.split()))
    missing = list(set(j.split()) - set(r.split()))
    return {
        "similarity": sim,
        "match_percent": round(sim * 100, 2),
        "matched_skills": matched,
        "missing_skills": missing
    }

def assign_badge_for_score(score: int):
    if score >= 90:
        return ["Diamond", "Top Performer"]
    if score >= 80:
        return ["Platinum"]
    if score >= 70:
        return ["Gold"]
    if score >= 60:
        return ["Silver"]
    if score >= 50:
        return ["Bronze"]
    return ["Rookie"]
