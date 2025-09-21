from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from app.services.auth_service import register_user, login_user, get_current_user

router = APIRouter(tags=["Auth"])
security = HTTPBearer()


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
async def register(payload: RegisterRequest):
    result = register_user(payload.name, payload.email, payload.password)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error"))
    return {"message": "User registered successfully", "user_id": result["user"]["id"]}


@router.post("/login")
async def login(payload: LoginRequest):
    result = login_user(payload.email, payload.password)
    if not result.get("success"):
        raise HTTPException(status_code=401, detail=result.get("error"))
    return {
        "message": "Login successful",
        "token": result["token"],
        "role": result["role"],
        "user": {
            "id": result["user"]["id"],
            "email": result["user"]["email"]
        }
    }


@router.get("/me")
async def me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Verify user token
        user_info = supabase.auth.get_user(token)
        if not user_info or not user_info.user:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Fetch profile using service role
        profile = get_current_user(str(user_info.user.id))

        return {
            "id": str(user_info.user.id),
            "email": user_info.user.email,
            "name": profile.get("name"),
            "role": profile.get("role", "user")
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
