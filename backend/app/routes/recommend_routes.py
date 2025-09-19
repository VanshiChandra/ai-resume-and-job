from fastapi import APIRouter, HTTPException
from app.services.recommend_service import ats_recommend, ai_recommend, combined_recommend

router = APIRouter(prefix="/recommend", tags=["Recommend"])

@router.get("/{resume_id}/{job_id}")
def recommend_ats(resume_id: str, job_id: str):
    return ats_recommend(resume_id, job_id)

@router.get("/{user_id}")
def recommend_ai(user_id: str):
    return ai_recommend(user_id)

@router.get("/combined/{user_id}/{resume_id}/{job_id}")
def recommend_both(user_id: str, resume_id: str, job_id: str):
    try:
        return combined_recommend(user_id, resume_id, job_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
