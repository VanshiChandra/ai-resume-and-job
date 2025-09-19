from fastapi import APIRouter, HTTPException
from app.models.schemas import MatchRequest
from app.services.matching_service import match_resume_with_job, rank_candidates, suggest_missing_skills

router = APIRouter(prefix="/matching", tags=["Matching"])

@router.post("/match")
def match(req: MatchRequest):
    """
    Match a resume with a job posting and return ATS-style score/details.
    """
    try:
        res = match_resume_with_job(req.resume_id, req.job_id)
        if not res:
            raise HTTPException(status_code=400, detail="Match failed")
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rank/{job_id}")
def rank(job_id: str):
    """
    Rank all candidates for a given job posting.
    """
    try:
        return rank_candidates(job_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/suggest/{resume_id}/{job_id}")
def suggest(resume_id: str, job_id: str):
    """
    Suggest missing skills for a resume compared to a specific job posting.
    """
    try:
        return suggest_missing_skills(resume_id, job_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
