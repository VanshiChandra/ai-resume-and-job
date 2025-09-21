from fastapi import APIRouter, HTTPException
from app.services.recommend_service import ats_recommend, ai_recommend, combined_recommend

router = APIRouter(prefix="/recommend", tags=["Recommend"])

@router.get("/ats/{resume_id}/{job_id}")
def recommend_ats(resume_id: str, job_id: str):
    """ATS-based recommendation: resume vs job"""
    return ats_recommend(resume_id, job_id)

@router.get("/ai/{user_id}")
def recommend_ai(user_id: str):
    """AI-based recommendation: roles from resume"""
    return ai_recommend(user_id)

@router.get("/combined/{user_id}/{resume_id}/{job_id}")
def recommend_both(user_id: str, resume_id: str, job_id: str):
    """Combined recommendation: ATS + AI"""
    try:
        return combined_recommend(user_id, resume_id, job_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
