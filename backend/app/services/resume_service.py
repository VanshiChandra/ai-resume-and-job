import uuid
from fastapi import UploadFile
from app.supabase_client import supabase
from app.utils.nlp_utils import extract_text_and_skills
from app.utils.storage_utils import upload_bytes_to_storage

async def process_resume(file: UploadFile, user_id: str, job_desc: str = ""):
    # read bytes
    content = await file.read()
    parsed = extract_text_and_skills(content, file.filename)
    skills = parsed["skills"]
    text = parsed["text"]

    # upload to storage
    key = f"resumes/{user_id}/{uuid.uuid4().hex}-{file.filename}"
    file_url = upload_bytes_to_storage(key, content, file.content_type)

    # insert resume record
    res = supabase.table("resumes").insert({
        "user_id": user_id,
        "content": text,
    }).select().execute()

    resume_id = None
    if res and getattr(res, "data", None):
        # supabase-py returns object with .data
        resume_id = res.data[0].get("id") if res.data else None

    # compute matches (async call)
    from app.services.matching_service import compute_matches_for_resume
    matches_info = compute_matches_for_resume(user_id, text)

    # store ai suggestions (best-effort)
    from app.services.ai_service import suggest_roles_by_skills
    suggested = suggest_roles_by_skills(skills)
    try:
        supabase.table("ai_suggestions").insert({
            "user_id": user_id,
            "resume_id": resume_id,
            "suggested_roles": suggested if isinstance(suggested, list) else [suggested]
        }).execute()
    except Exception:
        pass

    return {"resume_id": resume_id, "file_url": file_url, "skills": skills, "matches": matches_info.get("matches"), "avg_score": matches_info.get("avg_score")}

def list_resumes(user_id: str):
    res = supabase.table("resumes").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return res.data if res and getattr(res, "data", None) else []

def get_resume(resume_id: str):
    res = supabase.table("resumes").select("*").eq("id", resume_id).single().execute()
    return res.data if res and getattr(res, "data", None) else {}

def delete_resume(resume_id: str):
    supabase.table("resumes").delete().eq("id", resume_id).execute()
    return {"ok": True}
