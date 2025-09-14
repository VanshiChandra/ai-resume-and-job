from fastapi import APIRouter, HTTPException
from app.models.schemas import RegisterRequest, LoginRequest
from app.services.auth_service import register_user, login_user, reset_password

router = APIRouter()


@router.post("/register")
def register(req: RegisterRequest):
    result = register_user(req.name, req.email, req.password)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Registration failed"))
    return {
        "message": "Registered successfully",
        "user": result.get("user")
    }


@router.post("/login")
def login(req: LoginRequest):
    result = login_user(req.email, req.password)
    if not result.get("success"):
        raise HTTPException(status_code=401, detail=result.get("error", "Login failed"))

    # frontend expects { token, isAdmin }
    return {
        "token": result.get("token"),
        "isAdmin": result.get("isAdmin", False)
    }


@router.post("/forgot-password")
def forgot_password(email: str):
    result = reset_password(email)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed"))
    return {"message": result.get("message")}
