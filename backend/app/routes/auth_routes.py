# backend/app/routes/auth_routes.py
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
import os

router = APIRouter(tags=["Auth"])
security = HTTPBearer()

# ---------------------------
# Initialize Supabase client
# ---------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------
# Request models
# ---------------------------
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ---------------------------
# Register user
# ---------------------------
@router.post("/register")
async def register_user(payload: RegisterRequest):
    try:
        # Step 1: Create user in Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": payload.email,
            "password": payload.password
        })
        user = getattr(auth_response, "user", None)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Supabase Auth user creation failed"
            )
        user_id = str(user.id)
        print("Supabase user created:", user_id)

        # Step 2: Insert into profiles table
        profile = {
            "id": user_id,
            "name": payload.name,
            "email": payload.email,
            "role": "user"
        }
        try:
            res = supabase.table("profiles").upsert(profile, on_conflict="id").execute()
            print("Profile upsert result:", res)
        except Exception as e:
            print("PROFILE INSERT ERROR:", e)
            raise HTTPException(status_code=500, detail=f"Failed to create profile: {str(e)}")

        return {"message": "User registered successfully", "user_id": user_id}

    except Exception as e:
        print("REGISTER ERROR:", e)
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


# ---------------------------
# Login user
# ---------------------------
@router.post("/login")
async def login_user(payload: LoginRequest):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": payload.email,
            "password": payload.password
        })
        user = getattr(auth_response, "user", None)
        session = getattr(auth_response, "session", None)

        if not user or not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid login credentials"
            )

        user_id = str(user.id)

        # Fetch profile to get role
        try:
            profile_res = supabase.table("profiles").select("role").eq("id", user_id).maybe_single().execute()
            profile = getattr(profile_res, "data", None)
            role = profile.get("role") if profile else "user"
        except Exception as e:
            print("PROFILE FETCH ERROR:", e)
            role = "user"

        return {
            "message": "Login successful",
            "token": session.access_token,
            "refresh_token": session.refresh_token,
            "user": {
                "id": user_id,
                "email": user.email,
                "role": role
            }
        }

    except Exception as e:
        print("LOGIN ERROR:", e)
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


# ---------------------------
# Get current user (/me)
# ---------------------------
@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user_info = supabase.auth.get_user(token)
        if not user_info or not getattr(user_info, "user", None):
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = str(user_info.user.id)
        email = user_info.user.email

        # Fetch profile
        profile_res = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        profile = getattr(profile_res, "data", None) or {}

        return {
            "id": user_id,
            "email": email,
            "name": profile.get("name"),
            "role": profile.get("role", "user")
        }

    except Exception as e:
        print("GET /me ERROR:", e)
        raise HTTPException(status_code=401, detail=f"Unauthorized: {str(e)}")
