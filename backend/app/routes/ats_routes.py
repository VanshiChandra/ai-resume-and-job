from fastapi import APIRouter, Depends
from app.services.ats_service import ats_match_resume
from app.supabase_client import supabase

router = APIRouter(prefix="/ats", tags=["ATS"])

@router.get("/matches/{user_id}")
def get_user_matches(user_id: str):
    """Fetch all ATS matches for a user"""
    res = supabase.table("job_matches").select("*").eq("user_id", user_id).execute()
    return res.data or []

@router.post("/match")
def create_match(user_id: str, job_id: str, score: int):
    """Store ATS resume match result"""
    return ats_match_resume(user_id, job_id, score)
