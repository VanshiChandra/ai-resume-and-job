from app.supabase_client import supabase
from app.utils.match_utils import assign_badge_for_score

def get_global_leaderboard():
    res = supabase.table("leaderboard") \
        .select("score, user_id, profiles(name,email)") \
        .order("score", desc=True) \
        .limit(100) \
        .execute()

    rows = res.data if res and getattr(res, "data", None) else []
    for r in rows:
        r["badges"] = assign_badge_for_score(r.get("score", 0))
    return rows

def get_job_leaderboard(job_id: str):
    res = supabase.table("job_matches") \
        .select("confidence, user_id, profiles(name,email)") \
        .eq("job_id", job_id) \
        .order("confidence", desc=True) \
        .limit(100) \
        .execute()

    return res.data if res and getattr(res, "data", None) else []

def get_user_badges(user_id: str):
    res = supabase.table("badges") \
        .select("*") \
        .eq("user_id", user_id) \
        .execute()

    return res.data if res and getattr(res, "data", None) else []
