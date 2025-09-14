# backend/app/services/admin_service.py
from app.supabase_client import supabase

def get_all_users():
    try:
        res = supabase.table("profiles").select("*").execute()
        return {"success": True, "data": getattr(res, "data", None) or res.get("data")}
    except Exception as e:
        return {"success": False, "error": str(e)}

def update_user_role(user_id: str, new_role: str):
    try:
        res = supabase.table("profiles").update({"role": new_role}).eq("id", user_id).execute()
        return {"success": True, "data": getattr(res, "data", None) or res.get("data")}
    except Exception as e:
        return {"success": False, "error": str(e)}
