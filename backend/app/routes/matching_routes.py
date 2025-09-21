from fastapi import APIRouter, HTTPException
from app.models.schemas import MatchRequest
from app.services.matching_service import match_resume_with_job, rank_candidates, suggest_missing_skills

router = APIRouter(prefix="/matching", tags=["Matching"])

# ============================
# Match a resume with a job
# ============================
@router.post("/match")
def match(req: MatchRequest):
    try:
        result = match_resume_with_job(req.resume_id, req.job_id)
        if not result:
            raise HTTPException(status_code=400, detail="Resume-job match failed")
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to match resume with job: {str(e)}")

# ============================
# Rank candidates for a job
# ============================
@router.get("/rank/{job_id}")
def rank(job_id: str):
    try:
        rankings = rank_candidates(job_id)
        if not rankings:
            raise HTTPException(status_code=404, detail="No candidate rankings found for this job")
        return {"success": True, "data": rankings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to rank candidates: {str(e)}")

# ============================
# Suggest missing skills for a resume
# ============================
@router.get("/suggest/{resume_id}/{job_id}")
def suggest(resume_id: str, job_id: str):
    try:
        suggestions = suggest_missing_skills(resume_id, job_id)
        if not suggestions:
            raise HTTPException(status_code=404, detail="No missing skill suggestions found")
        return {"success": True, "data": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to suggest missing skills: {str(e)}")
