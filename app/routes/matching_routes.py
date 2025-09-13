from fastapi import APIRouter, HTTPException, Form
from app.services.matching_service import match_resume_with_job, rank_candidates, suggest_missing_skills

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
    return suggest_missing_skills(resume_id, job_id)
