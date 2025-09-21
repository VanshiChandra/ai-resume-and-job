from fastapi import APIRouter, HTTPException
from app.services.recommend_service import ats_recommend, ai_recommend, combined_recommend

router = APIRouter(prefix="/recommend", tags=["Recommend"])

# ============================
# ATS-based recommendation
# ============================
@router.get("/ats/{resume_id}/{job_id}")
def recommend_ats(resume_id: str, job_id: str):
    try:
        result = ats_recommend(resume_id, job_id)
        if not result:
            raise HTTPException(status_code=404, detail="No ATS recommendation found")
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ATS recommendation failed: {str(e)}")

# ============================
# AI-based recommendation
# ============================
@router.get("/ai/{user_id}")
def recommend_ai(user_id: str):
    try:
        result = ai_recommend(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="No AI recommendation found")
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI recommendation failed: {str(e)}")

# ============================
# Combined recommendation (ATS + AI)
# ============================
@router.get("/combined/{user_id}/{resume_id}/{job_id}")
def recommend_both(user_id: str, resume_id: str, job_id: str):
    try:
        result = combined_recommend(user_id, resume_id, job_id)
        if not result:
            raise HTTPException(status_code=404, detail="No combined recommendation found")
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Combined recommendation failed: {str(e)}")
