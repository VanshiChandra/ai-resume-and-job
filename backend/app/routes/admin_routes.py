# backend/app/routes/admin_routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_admin
from app.services import admin_service

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
def admin_dashboard(admin=Depends(get_current_admin)):
    return {"message": "Welcome Admin", "admin_id": admin["id"]}

@router.get("/users")
def list_users(admin=Depends(get_current_admin)):
    result = admin_service.get_all_users()
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result["data"]

@router.put("/users/{user_id}/role")
def set_user_role(user_id: str, new_role: str, admin=Depends(get_current_admin)):
    if new_role not in ("user", "admin"):
        raise HTTPException(status_code=400, detail="Invalid role")
    result = admin_service.update_user_role(user_id, new_role)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return {"ok": True, "user_id": user_id, "new_role": new_role}
