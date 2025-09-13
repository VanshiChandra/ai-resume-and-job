from app.supabase_client import supabase
from app.utils.nlp_utils import extract_skills_from_text

def add_job(data: dict):
    title = data.get("title")
    description = data.get("description")
    skills = data.get("required_skills") or extract_skills_from_text(description)

    res = supabase.table("jobs").insert({
        "title": title,
        "description": description,
        "skills": skills
    }).select().execute()

    return {"ok": True, "job": res.data[0] if res and getattr(res, "data", None) else None}

def list_jobs():
    res = supabase.table("jobs").select("*").order("created_at", desc=True).execute()
    return res.data if res and getattr(res, "data", None) else []

def get_job_by_id(job_id: str):
    res = supabase.table("jobs").select("*").eq("id", job_id).single().execute()
    return res.data if res and getattr(res, "data", None) else None

def delete_job(job_id: str):
    supabase.table("jobs").delete().eq("id", job_id).execute()
    return {"ok": True}
