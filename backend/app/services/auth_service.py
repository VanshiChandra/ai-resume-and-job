import os
from app.supabase_client import supabase

# ============================
# User Registration
# ============================
def register_user(name: str, email: str, password: str, role: str = "user"):
    """
    Register a new user with Supabase Auth and store their profile with role.
    """
    try:
        # Sign up user
        res = supabase.auth.sign_up({"email": email, "password": password})
        user = getattr(res, "user", None) or (res.get("user") if isinstance(res, dict) else None)

        if not user:
            return {"success": False, "error": "User registration failed"}

        user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id", None)

        # Insert profile record (matching auth.users.id for RLS)
        supabase.table("profiles").upsert({
            "id": user_id,
            "email": email,
            "name": name,
            "role": role
        }, on_conflict="id").execute()

        return {"success": True, "user": user, "role": role}

    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================
# User Login
# ============================
def login_user(email: str, password: str):
    """
    Login with Supabase Auth, return access token + role + user info.
    """
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        session = getattr(res, "session", None) or (res.get("session") if isinstance(res, dict) else None)
        user = getattr(res, "user", None) or (res.get("user") if isinstance(res, dict) else None)

        if not user or not session:
            return {"success": False, "error": "Invalid login credentials"}

        user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id", None)

        # Fetch profile to get role
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
            "access_token": session.get("access_token") if isinstance(session, dict) else getattr(session, "access_token", None),
            "refresh_token": session.get("refresh_token") if isinstance(session, dict) else getattr(session, "refresh_token", None),
            "user": user,
            "role": role
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================
# Get current user from token
# ============================
def get_current_user(token: str):
    """
    Get user info and profile by verifying access token via Supabase.
    """
    try:
        user_info = supabase.auth.get_user(token)
        if not user_info or not user_info.user:
            return {"success": False, "error": "Invalid token"}

        user_id = str(user_info.user.id)

        # Fetch profile to get full info
        profile_res = supabase.table("profiles").select("*").eq("id", user_id).maybe_single().execute()
        profile = profile_res.data if hasattr(profile_res, "data") else profile_res.get("data") or {}

        return {
            "success": True,
            "user": {
                "id": user_id,
                "email": user_info.user.email,
                "name": profile.get("name"),
                "role": profile.get("role", "user")
            }
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================
# Reset password
# ============================
def reset_password(email: str):
    """
    Trigger Supabase password reset email.
    """
    try:
        supabase.auth.reset_password_for_email(email)
        return {"success": True, "message": "Password reset initiated"}
    except Exception as e:
        return {"success": False, "error": str(e)}
