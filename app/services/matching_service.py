from app.supabase_client import supabase
from app.utils.match_utils import match_resume_to_job_text

def compute_matches_for_resume(user_id: str, resume_text: str):
    jobs_res = supabase.table("jobs").select("*").execute()
    jobs = jobs_res.data if jobs_res and getattr(jobs_res, "data", None) else []
    results = []
    total = 0.0
    for job in jobs:
        m = match_resume_to_job_text(resume_text, job.get("description",""))
        score = float(m.get("match_percent", 0))
        total += score
        results.append({
            "job_id": job.get("id"),
            "job_title": job.get("title"),
            "score": score,
            "missing_skills": m.get("missing_skills"),
            "matched_skills": m.get("matched_skills")
        })
        # persist match
        try:
            supabase.table("job_matches").insert({
                "resume_id": None,
                "matched_role": job.get("title"),
                "confidence": score
            }).execute()
        except Exception:
            pass
    avg = round(total / len(jobs), 2) if jobs else 0.0
    # upsert leaderboard
    try:
        # compute user's existing or insert
        supabase.table("leaderboard").upsert({"user_id": user_id, "points": int(avg)}).execute()
    except Exception:
        pass
    return {"matches": results, "avg_score": avg}

def match_resume_with_job(resume_id: str, job_id: str):
    r = supabase.table("resumes").select("content").eq("id", resume_id).single().execute()
    j = supabase.table("jobs").select("description,title").eq("id", job_id).single().execute()
    if not r or not j or not getattr(r, "data", None) or not getattr(j, "data", None):
        return None
    resume_text = r.data.get("content", "")
    job_text = j.data.get("description", "")
    m = match_resume_to_job_text(resume_text, job_text)
    return m

def rank_candidates(job_id: str):
    res = supabase.table("job_matches").select("resume_id, confidence").eq("matched_role", job_id).order("confidence", desc=True).execute()
    return res.data if res and getattr(res, "data", None) else []
