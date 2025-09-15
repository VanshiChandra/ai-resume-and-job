import os
from fastapi import APIRouter, HTTPException
from app.models.schemas import RegisterRequest, LoginRequest
from supabase import create_client

router = APIRouter()

# Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # service role key for admin ops
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@router.post("/register")
def register(req: RegisterRequest):
    try:
        # Create user in Supabase Auth (directly with admin API)
        auth_res = supabase.auth.admin.create_user({
            "email": req.email,
            "password": req.password,
            "email_confirm": True
        })

        if not auth_res or not auth_res.user:
            raise HTTPException(status_code=400, detail="Registration failed")

        user_id = auth_res.user.id

        # Create profile entry
        profile_res = supabase.table("profiles").insert({
            "id": user_id,
            "name": req.name,
            "email": req.email,
            "role": "user"
        }).execute()

        if profile_res.error:
            raise HTTPException(
                status_code=400,
                detail=f"Profile creation failed: {profile_res.error.message}"
            )

        return {
            "message": "Registered successfully",
            "user": {"id": user_id, "email": req.email, "name": req.name}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.post("/login")
def login(req: LoginRequest):
    try:
        # Sign in with Supabase
        auth_res = supabase.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password
        })

        if not auth_res or not getattr(auth_res, "session", None):
            raise HTTPException(status_code=401, detail="Login failed: invalid credentials")

        access_token = auth_res.session.access_token
        user_id = auth_res.user.id

        # Fetch role from profiles
        profile_res = supabase.table("profiles").select("role").eq("id", user_id).single().execute()
        if profile_res.error or not profile_res.data:
            raise HTTPException(status_code=401, detail="Profile not found")

        role = profile_res.data.get("role", "user")

        return {
            "token": access_token,   # frontend stores this instead of custom JWT
            "role": role,
            "user": {"id": user_id, "email": req.email, "role": role}
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error during login: {str(e)}")
