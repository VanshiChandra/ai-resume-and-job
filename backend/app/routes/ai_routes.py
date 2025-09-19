from fastapi import APIRouter, HTTPException
from typing import List
from app.services.ai_service import suggest_roles_by_skills, suggest_roles_for_user, fetch_user_ai_suggestions

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/suggest-from-skills")
def suggest_from_skills(skills: List[str]):
    return suggest_roles_by_skills(skills)

@router.get("/suggest-for-user/{user_id}")
def suggest_for_user(user_id: str):
    try:
        return suggest_roles_for_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/suggestions/{user_id}")
def get_user_ai_suggestions(user_id: str):
    """
    Fetch past AI role suggestions for a user.
    """
    try:
        return fetch_user_ai_suggestions(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
