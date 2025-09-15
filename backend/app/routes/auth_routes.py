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
        # ✅ Create user in Supabase Auth (admin API)
        auth_res = supabase.auth.admin.create_user({
            "email": req.email,
            "password": req.password,
            "email_confirm": True
        })

        if not auth_res or not getattr(auth_res, "user", None):
            raise HTTPException(status_code=400, detail="Registration failed: no user returned")

        user_id = auth_res.user.id

        # ✅ Insert into profiles
        profile_res = supabase.table("profiles").insert({
            "id": user_id,
            "name": req.name,
            "email": req.email,
            "role": "user"
        }).execute()

        if getattr(profile_res, "error", None):
            print("❌ Profile insert error:", profile_res.error)
            raise HTTPException(status_code=400, detail="Profile creation failed")

        return {
            "message": "Registered successfully",
            "user": {"id": user_id, "email": req.email, "name": req.name}
        }

    except Exception as e:
        print("❌ Registration error:", str(e))
        raise HTTPException(status_code=500, detail="Unexpected error during registration")


@router.post("/login")
def login(req: LoginRequest):
    try:
        # ✅ Sign in
        auth_res = supabase.auth.sign_in_with_password({
            "email": req.email,
            "password": req.password
        })

        if not auth_res or not getattr(auth_res, "session", None):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = auth_res.session.access_token
        user_id = auth_res.user.id

        # ✅ Fetch role from profiles
        profile_res = supabase.table("profiles").select("role").eq("id", user_id).single().execute()

        if getattr(profile_res, "error", None) or not profile_res.data:
            print("❌ Profile fetch error:", profile_res.error if profile_res.error else "No data")
            raise HTTPException(status_code=401, detail="Profile not found")

        role = profile_res.data.get("role", "user")

        return {
            "token": access_token,
            "role": role,
            "user": {"id": user_id, "email": req.email, "role": role}
        }

    except Exception as e:
        print("❌ Login error:", str(e))
        raise HTTPException(status_code=500, detail="Unexpected error during login")
