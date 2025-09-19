from app.supabase_client import supabase
from app.utils.match_utils import assign_badge_for_score


def get_global_leaderboard():
    """
    Fetch the global leaderboard sorted by score.
    Includes user profile info and assigns badges.
    """
    res = supabase.table("leaderboard") \
        .select("score, user_id, profiles(name,email)") \
        .order("score", desc=True) \
        .limit(100) \
        .execute()

    rows = res.data if res and getattr(res, "data", None) else []

    leaderboard = []
    for r in rows:
        leaderboard.append({
            "user_id": r.get("user_id"),
            "name": r.get("profiles", {}).get("name"),
            "email": r.get("profiles", {}).get("email"),
            "score": r.get("score", 0),
            "badges": assign_badge_for_score(r.get("score", 0))
        })
    return leaderboard


def get_job_leaderboard(job_id: str):
    """
    Fetch leaderboard for a specific job.
    Sorted by match confidence, includes badges.
    """
    res = supabase.table("job_matches") \
        .select("confidence, user_id, profiles(name,email)") \
        .eq("job_id", job_id) \
        .order("confidence", desc=True) \
        .limit(100) \
        .execute()

    rows = res.data if res and getattr(res, "data", None) else []

    leaderboard = []
    for r in rows:
        leaderboard.append({
            "user_id": r.get("user_id"),
            "name": r.get("profiles", {}).get("name"),
            "email": r.get("profiles", {}).get("email"),
            "confidence": r.get("confidence", 0),
            "badges": assign_badge_for_score(r.get("confidence", 0))
        })
    return leaderboard


def get_user_badges(user_id: str):
    """
    Fetch all badges earned by a specific user.
    """
    res = supabase.table("badges") \
        .select("*") \
        .eq("user_id", user_id) \
        .execute()

    badges = res.data if res and getattr(res, "data", None) else []
    return badges
