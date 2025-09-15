from fastapi import APIRouter, HTTPException
from app.models.schemas import RegisterRequest, LoginRequest
from supabase import create_client
import os

router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@router.post("/register")
def register(req: RegisterRequest):
    try:
        # Try creating user
        auth_res = supabase.auth.admin.create_user({
            "email": req.email,
            "password": req.password,
            "email_confirm": True
        })

        if not auth_res or not auth_res.user:
            raise HTTPException(status_code=400, detail="Registration failed")

        user_id = auth_res.user.id

        # Create profile
        supabase.table("profiles").insert({
            "id": user_id,
            "name": req.name,
            "email": req.email,
            "role": "user"
        }).execute()

        return {"message": "Registered successfully"}

    except Exception as e:
        error_msg = str(e)

        if "already been registered" in error_msg:
            raise HTTPException(status_code=409, detail="Email already registered")

        raise HTTPException(status_code=500, detail=f"Unexpected error: {error_msg}")


@router.post("/login")
def login(req: LoginRequest):
    try:
        auth_res = supabase.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password
        })

        if not auth_res or not getattr(auth_res, "session", None):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = auth_res.session.access_token
        user_id = auth_res.user.id

        # Fetch role
        profile_res = supabase.table("profiles").select("role").eq("id", user_id).single().execute()
        if profile_res.error or not profile_res.data:
            raise HTTPException(status_code=404, detail="Profile not found")

        return {
            "token": access_token,
            "role": profile_res.data.get("role", "user"),
            "user": {"id": user_id, "email": req.email}
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error during login: {str(e)}")
