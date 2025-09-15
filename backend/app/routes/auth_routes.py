from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
import os

router = APIRouter(prefix="/api/auth", tags=["Auth"])

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

    if auth_response.get("error"):
        error_msg = auth_response["error"]["message"]
        if "already registered" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Auth error: {error_msg}"
        )

    user = auth_response.get("user")
    if not user:
        raise HTTPException(status_code=500, detail="User creation failed in Supabase Auth.")

    user_id = user["id"]

    # Step 2: Insert into profiles table if not exists
    profile = {
        "id": user_id,
        "name": payload.name,
        "email": payload.email,
        "role": "user"
    }

    try:
        # Use UPSERT to avoid duplicate insert issues
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

    if auth_response.get("error"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials"
        )

    session = auth_response.get("session")
    user = auth_response.get("user")

    if not session or not user:
        raise HTTPException(status_code=500, detail="Login failed due to missing session.")

    return {
        "message": "Login successful",
        "access_token": session["access_token"],
        "refresh_token": session["refresh_token"],
        "user": {
            "id": user["id"],
            "email": user["email"]
        }
    }
