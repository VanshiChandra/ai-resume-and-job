from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from app.services import auth_service

router = APIRouter(tags=["Auth"])
security = HTTPBearer()

# ============================
# Request models
# ============================
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ============================
# Register
# ============================
@router.post("/register")
async def register_user(payload: RegisterRequest):
    result = auth_service.register_user(payload.name, payload.email, payload.password)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("error"))
    return {"message": "User registered successfully", "user": result["user"], "role": result["role"]}

# ============================
# Login
# ============================
@router.post("/login")
async def login_user(payload: LoginRequest):
    result = auth_service.login_user(payload.email, payload.password)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=result.get("error"))
    
    return {
        "message": "Login successful",
        "access_token": result.get("token"),
        "user": result.get("user"),
        "role": result.get("role")
    }

# ============================
# Get current user
# ============================
@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    from app.supabase_client import supabase

    try:
        user_info = supabase.auth.get_user(token)
        if not user_info or not getattr(user_info, "user", None):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        # Fetch full profile from Supabase table
        profile_res = supabase.table("profiles").select("*").eq("id", str(user_info.user.id)).maybe_single().execute()
        profile = getattr(profile_res, "data", None) or {}
        
        return {
            "id": str(user_info.user.id),
            "email": user_info.user.email,
            "name": profile.get("name"),
            "role": profile.get("role", "user")
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
