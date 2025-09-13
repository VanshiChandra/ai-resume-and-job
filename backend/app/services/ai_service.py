import os
from typing import List
import json
from app.supabase_client import supabase
from app.config import OPENAI_API_KEY
import openai

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

FALLBACK = ["Software Engineer", "Data Engineer", "DevOps Engineer"]

def suggest_roles_by_skills(skills: List[str]):
    # Return list of 3 role strings
    skills_text = ", ".join(skills or [])
    if not OPENAI_API_KEY:
        # simple heuristic fallback
        t = skills_text.lower()
        if "python" in t or "ml" in t:
            return ["Machine Learning Engineer", "Data Scientist", "ML Engineer"]
        if "react" in t or "javascript" in t:
            return ["Frontend Engineer", "Full-Stack Engineer", "React Developer"]
        return FALLBACK
    try:
        prompt = f"Given these skills: {skills_text}. Suggest 5 job roles (return JSON array)."
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            max_tokens=150
        )
        text = resp.choices[0].message.content.strip()
        # try to parse
        try:
            arr = json.loads(text)
            return arr if isinstance(arr, list) else [text]
        except Exception:
            # fallback: split lines
            lines = [l.strip("- ").strip() for l in text.splitlines() if l.strip()]
            return lines[:5] if lines else [text]
    except Exception:
        # final fallback
        return FALLBACK

def suggest_roles_for_user(user_id: str):
    res = supabase.table("resumes").select("content").eq("user_id", user_id).order("created_at", desc=True).limit(1).execute()
    content = res.data[0]["content"] if res and getattr(res, "data", None) and res.data else ""
    skills = []
    if content:
        from app.utils.nlp_utils import extract_skill_words
        skills = extract_skill_words(content)
    roles = suggest_roles_by_skills(skills)
    # persist
    try:
        supabase.table("ai_suggestions").insert({"user_id": user_id, "suggested_roles": roles}).execute()
    except Exception:
        pass
    return {"suggested_roles": roles}
