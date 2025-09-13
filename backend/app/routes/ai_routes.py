from fastapi import APIRouter, HTTPException
from typing import List
from app.services.ai_service import suggest_roles_by_skills, suggest_roles_for_user

router = APIRouter()

@router.post("/suggest-from-skills")
def suggest_from_skills(skills: List[str]):
    return suggest_roles_by_skills(skills)

@router.get("/suggest-for-user/{user_id}")
def suggest_for_user(user_id: str):
    try:
        return suggest_roles_for_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
