import os
import jwt
import datetime
from app.supabase_client import supabase

JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")
JWT_ALGORITHM = "HS256"


def create_jwt(email: str, is_admin: bool = False):
    payload = {
        "sub": email,
        "isAdmin": is_admin,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def register_user(name: str, email: str, password: str):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})

        user = None
        if hasattr(res, "user") and res.user:
            user = res.user
        elif isinstance(res, dict) and res.get("user"):
            user = res.get("user")

        if user:
            supabase.table("users").insert({
                "id": user.get("id") if isinstance(user, dict) else user.id,
                "email": email,
                "name": name,
                "isAdmin": False   # default: normal user
            }).execute()

        return {"success": True, "user": user}
    except Exception as e:
        return {"success": False, "error": str(e)}


def login_user(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        user = None
        if hasattr(res, "user") and res.user:
            user = res.user
        elif isinstance(res, dict) and res.get("user"):
            user = res.get("user")

        if not user:
            return {"success": False, "error": "Invalid credentials"}

        # fetch from users table to get role/isAdmin
        user_record = supabase.table("users").select("*").eq("email", email).execute()
        user_data = user_record.data[0] if user_record.data else {}
        is_admin = user_data.get("isAdmin", False)

        token = create_jwt(email, is_admin)

        return {
            "success": True,
            "token": token,
            "isAdmin": is_admin
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def reset_password(email: str):
    try:
        supabase.auth.reset_password_for_email(email)
        return {"success": True, "message": "Password reset initiated"}
    except Exception as e:
        return {"success": False, "error": str(e)}
