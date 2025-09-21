from fastapi import APIRouter, HTTPException
from app.services.leaderboard_service import (
    get_global_leaderboard, 
    get_job_leaderboard, 
    get_user_badges
)

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

# ============================
# Global leaderboard
# ============================
@router.get("/global")
def fetch_global_leaderboard():
    try:
        leaderboard = get_global_leaderboard()
        if not leaderboard:
            raise HTTPException(status_code=404, detail="No leaderboard data found")
        return {"success": True, "data": leaderboard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch global leaderboard: {str(e)}")

# ============================
# Job-specific leaderboard
# ============================
@router.get("/job/{job_id}")
def fetch_job_leaderboard(job_id: str):
    try:
        leaderboard = get_job_leaderboard(job_id)
        if not leaderboard:
            raise HTTPException(status_code=404, detail="No leaderboard data found for this job")
        return {"success": True, "data": leaderboard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch job leaderboard: {str(e)}")

# ============================
# User badges
# ============================
@router.get("/badges/{user_id}")
def fetch_user_badges(user_id: str):
    try:
        badges = get_user_badges(user_id)
        if not badges:
            raise HTTPException(status_code=404, detail="No badges found for this user")
        return {"success": True, "data": badges}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user badges: {str(e)}")
