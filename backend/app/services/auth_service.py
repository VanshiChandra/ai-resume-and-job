# backend/app/services/auth_service.py
import os
from app.supabase_client import supabase

def register_user(name: str, email: str, password: str, role: str = "user"):
    """
    Register a new user with Supabase Auth and store their profile with role.
    """
    try:
        # Sign up using Supabase Auth
        res = supabase.auth.sign_up({"email": email, "password": password})
        user = getattr(res, "user", None) or (res.get("user") if isinstance(res, dict) else None)

        if not user:
            return {"success": False, "error": "User registration failed"}

        user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id", None)

        # Insert profile record (must match auth.users.id for RLS)
        supabase.table("profiles").insert({
            "id": user_id,
            "email": email,
            "name": name,
            "role": role
        }).execute()

        return {"success": True, "user": user, "role": role}

    except Exception as e:
        return {"success": False, "error": str(e)}


def login_user(email: str, password: str):
    """
    Login with Supabase Auth, return token + role.
    """
    try:
        # Authenticate user
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        session = getattr(res, "session", None) or (res.get("session") if isinstance(res, dict) else None)
        user = getattr(res, "user", None) or (res.get("user") if isinstance(res, dict) else None)

        if not user or not session:
            return {"success": False, "error": "Invalid login credentials"}

        user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id", None)

        # Fetch profile to get role
        profile = None
        role = "user"
        try:
            if user_id:
                profile_res = supabase.table("profiles").select("role").eq("id", user_id).maybe_single().execute()
                profile = profile_res.data if hasattr(profile_res, "data") else profile_res.get("data")
                if profile and "role" in profile:
                    role = profile["role"]
        except Exception:
            pass

        return {
            "success": True,
            "token": session.get("access_token") if isinstance(session, dict) else getattr(session, "access_token", None),
            "user": user,
            "role": role
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def reset_password(email: str):
    """
    Trigger Supabase password reset email.
    """
    try:
        supabase.auth.reset_password_for_email(email)
        return {"success": True, "message": "Password reset initiated"}
    except Exception as e:
        return {"success": False, "error": str(e)}
