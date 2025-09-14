# backend/app/routes/auth_routes.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import RegisterRequest, LoginRequest
from app.services.auth_service import register_user, login_user

router = APIRouter()

@router.post("/register")
def register(req: RegisterRequest):
    result = register_user(req.name, req.email, req.password)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Registration failed"))

    user = result.get("user")
    role = result.get("role", "user")

    return {
        "message": "Registered successfully",
        "user": {
            "id": user.get("id") if isinstance(user, dict) else getattr(user, "id", None),
            "email": req.email,
            "name": req.name,
            "role": role,
        },
    }

@router.post("/login")
def login(req: LoginRequest):
    result = login_user(req.email, req.password)
    if not result.get("success"):
        raise HTTPException(status_code=401, detail=result.get("error", "Login failed"))

    user = result.get("user")
    role = result.get("role", "user")
    token = result.get("token")

    user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id", None)

    return {
        "token": token,
        "isAdmin": role == "admin",   # 👈 for frontend localStorage
        "role": role,
        "user": {
            "id": user_id,
            "email": req.email,
            "role": role,
        },
    }
