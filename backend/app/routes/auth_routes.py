from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
router = APIRouter(tags=["Auth"])
security = HTTPBearer()
# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


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
    # Step 1: Create user in Supabase Auth
    auth_response = supabase.auth.sign_up({
        "email": payload.email,
        "password": payload.password
    })

    if auth_response.user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User creation failed in Supabase Auth."
        )

    user_id = str(auth_response.user.id)

    # Step 2: Insert into profiles table if not exists
    profile = {
        "id": user_id,
        "name": payload.name,
        "email": payload.email,
        "role": "user"
    }

    try:
        supabase.table("profiles").upsert(profile, on_conflict="id").execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create profile: {str(e)}")

    return {"message": "User registered successfully", "user_id": user_id}


# ============================
# Login
# ============================
@router.post("/login")
async def login_user(payload: LoginRequest):
    # Authenticate user
    auth_response = supabase.auth.sign_in_with_password({
        "email": payload.email,
        "password": payload.password
    })

    if auth_response.user is None or auth_response.session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials"
        )

    return {
        "message": "Login successful",
        "access_token": auth_response.session.access_token,
        "refresh_token": auth_response.session.refresh_token,
        "user": {
            "id": str(auth_response.user.id),
            "email": auth_response.user.email
        }
    }
@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    # Verify token via Supabase
    try:
        user_info = supabase.auth.get_user(token)
        if not user_info or not user_info.user:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Optionally, fetch full profile from Supabase table
    profile_res = supabase.table("profiles").select("*").eq("id", str(user_info.user.id)).single().execute()
    profile = profile_res.data if profile_res and getattr(profile_res, "data", None) else {}

    return {
        "id": str(user_info.user.id),
        "email": user_info.user.email,
        "name": profile.get("name"),
        "role": profile.get("role", "user")
    }