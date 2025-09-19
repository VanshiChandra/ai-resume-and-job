from fastapi import APIRouter, HTTPException
from app.services.leaderboard_service import (
    get_global_leaderboard, 
    get_job_leaderboard, 
    get_user_badges
)

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

@router.get("/global")
def fetch_global_leaderboard():
    """
    Get the global leaderboard across all users.
    """
    try:
        leaderboard = get_global_leaderboard()
        if leaderboard is None:
            raise HTTPException(status_code=404, detail="No leaderboard data found")
        return leaderboard
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/job/{job_id}")
def fetch_job_leaderboard(job_id: str):
    """
    Get leaderboard specific to a job.
    """
    try:
        leaderboard = get_job_leaderboard(job_id)
        if leaderboard is None:
            raise HTTPException(status_code=404, detail="No leaderboard data found for this job")
        return leaderboard
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/badges/{user_id}")
def fetch_user_badges(user_id: str):
    """
    Get all badges earned by a user.
    """
    try:
        badges = get_user_badges(user_id)
        if badges is None:
            raise HTTPException(status_code=404, detail="No badges found for this user")
        return badges
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
