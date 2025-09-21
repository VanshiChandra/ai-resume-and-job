import uuid
from fastapi import UploadFile, HTTPException
from app.utils.nlp_utils import extract_text_and_skills
from app.utils.match_utils import match_resume_to_job_text
from app.supabase_client import supabase


def ats_match_resume(user_id: str, job_id: str = None, score: float = 0.0, matched_skills=None, missing_skills=None):
    """Save ATS match result for a resume vs job"""
    matched_skills = matched_skills or []
    missing_skills = missing_skills or []

    supabase.table("job_matches").insert({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "job_id": job_id,
        "resume_id": None,  # ad-hoc resume
        "confidence": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }).execute()

    return {
        "user_id": user_id,
        "job_id": job_id,
        "confidence": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }


async def run_ats_check(file: UploadFile, job_desc: str, user_id: str = None, persist: bool = False):
    """
    ✅ Run ATS check:
       - Parse resume text + skills
       - Compare with job description (full-text)
       - Compute match score, matched skills, missing skills
       - Optionally save result into job_matches table
    """
    try:
        # Read file content
        content = await file.read()
        parsed = extract_text_and_skills(content, file.filename)

        resume_text = parsed.get("text", "")

        # Use full-text matching utility
        match_result = match_resume_to_job_text(resume_text, job_desc)
        score = float(match_result.get("match_percent", 0))
        matched = match_result.get("matched_skills", [])
        missing = match_result.get("missing_skills", [])

        result = {
            "resume_text": resume_text[:1000],  # preview only
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing,
        }

        # Persist result via helper function if requested
        if persist and user_id:
            ats_match_resume(
                user_id=user_id,
                score=score,
                matched_skills=matched,
                missing_skills=missing
            )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ATS check failed: {str(e)}")
