from fastapi import APIRouter, HTTPException, Form
from app.services.matching_service import match_resume_with_job, rank_candidates, suggest_missing_skills
from app.supabase_client import supabase

router = APIRouter()

@router.post("/match")
def match(resume_id: str = Form(...), job_id: str = Form(...)):
    res = match_resume_with_job(resume_id, job_id)
    if not res:
        raise HTTPException(status_code=400, detail="Match failed")
    return res

@router.get("/rank/{job_id}")
def rank(job_id: str):
    return rank_candidates(job_id)

@router.get("/suggest/{resume_id}/{job_id}")
def suggest(resume_id: str, job_id: str):
    # Fetch resume and job content
    r = supabase.table("resumes").select("content").eq("id", resume_id).single().execute()
    j = supabase.table("jobs").select("description").eq("id", job_id).single().execute()
    
    if not r or not j or not getattr(r, "data", None) or not getattr(j, "data", None):
        raise HTTPException(status_code=400, detail="Could not fetch resume or job")
    
    resume_text = r.data.get("content", "")
    job_text = j.data.get("description", "")
    
    missing_skills = suggest_missing_skills(resume_text, job_text)
    return {"missing_skills": missing_skills}
