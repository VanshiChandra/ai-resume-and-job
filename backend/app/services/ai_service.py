import os
import json
from typing import List
from app.supabase_client import supabase
from app.config import OPENAI_API_KEY
import openai
from app.utils.nlp_utils import extract_skill_words  # moved to top

# Configure OpenAI API key
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

FALLBACK = ["Software Engineer", "Data Engineer", "DevOps Engineer"]

def suggest_roles_by_skills(skills: List[str]):
    """
    Suggest job roles based on a list of skills.
    Returns a list of role strings.
    """
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
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=150
        )

        # safer content extraction
        text = resp.choices[0].message.get("content", "").strip()

        # try parsing as JSON
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
    """
    Suggest job roles for a specific user based on their latest resume.
    Extracts skills -> suggests roles -> persists in ai_suggestions.
    """
    res = supabase.table("resumes") \
        .select("parsed_text") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .limit(1) \
        .execute()

    content = res.data[0]["parsed_text"] if res and getattr(res, "data", None) and res.data else ""
    skills = extract_skill_words(content) if content else []
    roles = suggest_roles_by_skills(skills)

    # persist suggestions
    try:
        supabase.table("ai_suggestions").insert({
            "user_id": user_id,
            "suggested_roles": roles  # ensure column is jsonb
        }).execute()
    except Exception:
        # don’t break flow if persistence fails
        pass

    return {"suggested_roles": roles}


def fetch_user_ai_suggestions(user_id: str):
    """
    Fetch latest AI-generated role suggestions for a user.
    Returns a list of suggestion records (up to 10).
    """
    res = supabase.table("ai_suggestions") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("created_at", desc=True) \
        .limit(10) \
        .execute()

    return res.data if res and getattr(res, "data", None) else []
