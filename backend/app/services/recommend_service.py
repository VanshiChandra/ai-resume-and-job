from app.services.matching_service import match_resume_with_job, suggest_missing_skills
from app.services.ai_service import suggest_roles_for_user

def ats_recommend(resume_id: str, job_id: str):
    """
    ATS style recommendation: match resume with job and list missing skills.
    """
    match_result = match_resume_with_job(resume_id, job_id)
    if not match_result:
        return {"score": 0, "missing_skills": []}

    missing_skills = suggest_missing_skills(resume_id, job_id)
    return {
        "score": match_result.get("score", 0),
        "missing_skills": missing_skills or []
    }

def ai_recommend(user_id: str):
    """
    AI-based career role recommendations for a user.
    """
    try:
        return suggest_roles_for_user(user_id)
    except Exception as e:
        return {"suggested_roles": [], "error": str(e)}

def combined_recommend(user_id: str, resume_id: str, job_id: str):
    """
    Combines ATS matching and AI role suggestions into one response.
    """
    ats = ats_recommend(resume_id, job_id)
    ai = ai_recommend(user_id)

    return {
        "ATS": ats,
        "AI": ai
    }
def recommend_roles(resume_text: str):
    """Simple mock AI role recommender (can be replaced with OpenAI, HuggingFace etc.)"""
    suggestions = [
        {"role": "Software Engineer", "confidence": 85},
        {"role": "Data Analyst", "confidence": 78},
        {"role": "Machine Learning Engineer", "confidence": 72},
    ]
    return suggestions
