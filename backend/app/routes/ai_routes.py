from fastapi import APIRouter, HTTPException
from typing import List
from app.services.ai_service import (
    suggest_roles_by_skills,
    suggest_roles_for_user,
    fetch_user_ai_suggestions
)

router = APIRouter(prefix="/ai", tags=["AI"])

# ============================
# Suggest roles based on a list of skills
# ============================
@router.post("/suggest-from-skills")
def suggest_from_skills(skills: List[str]):
    try:
        result = suggest_roles_by_skills(skills)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to suggest roles: {str(e)}")

# ============================
# Suggest roles for a specific user
# ============================
@router.get("/suggest-for-user/{user_id}")
def suggest_for_user(user_id: str):
    try:
        result = suggest_roles_for_user(user_id)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to suggest roles for user: {str(e)}")

# ============================
# Fetch past AI suggestions for a user
# ============================
@router.get("/suggestions/{user_id}")
def get_user_ai_suggestions(user_id: str):
    try:
        result = fetch_user_ai_suggestions(user_id)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch AI suggestions: {str(e)}")
