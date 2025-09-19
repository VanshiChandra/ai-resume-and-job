from fastapi import APIRouter
from app.services.leaderboard_service import (
    get_global_leaderboard, 
    get_job_leaderboard, 
    get_user_badges
)

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

@router.get("/global")
def global_leaderboard():
    return get_global_leaderboard()

@router.get("/job/{job_id}")
def job_leaderboard(job_id: str):
    return get_job_leaderboard(job_id)

@router.get("/badges/{user_id}")
def user_badges(user_id: str):
    return get_user_badges(user_id)
