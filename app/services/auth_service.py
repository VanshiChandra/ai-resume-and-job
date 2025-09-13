from app.supabase_client import supabase

def register_user(name: str, email: str, password: str):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        # supabase-py returns object; res.user in older versions; handle generically
        user = None
        if hasattr(res, "user") and res.user:
            user = res.user
        elif isinstance(res, dict) and res.get("user"):
            user = res.get("user")

        if user:
            supabase.table("users").insert({
                "id": user.get("id") if isinstance(user, dict) else user.id,
                "email": email,
                "name": name
            }).execute()
        return {"success": True, "user": user}
    except Exception as e:
        return {"success": False, "error": str(e)}

def login_user(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        # res.session / res.user handling - return raw res
        return {"success": True, "session": getattr(res, "session", None) or (res.get("data") if isinstance(res, dict) else None), "user": getattr(res, "user", None) or (res.get("user") if isinstance(res, dict) else None)}
    except Exception as e:
        return {"success": False, "error": str(e)}

def reset_password(email: str):
    try:
        # For supabase-py, method may vary; use the REST call if needed
        res = supabase.auth.reset_password_for_email(email)
        return {"success": True, "message": "Password reset initiated"}
    except Exception as e:
        return {"success": False, "error": str(e)}
