import uuid
from fastapi import UploadFile, HTTPException
from app.supabase_client import supabase
from app.utils.storage_utils import upload_bytes_to_storage
from app.utils.nlp_utils import extract_text_and_skills
from app.services.ai_service import suggest_roles_by_skills
from app.services.matching_service import compute_matches_for_resume


async def upload_resume(file: UploadFile, user_id: str, job_desc: str = ""):
    
    
    try:
        # Read file content
        content = await file.read()

        # Extract text and skills using NLP utils
        parsed = extract_text_and_skills(content, file.filename)
        skills = parsed["skills"]
        text = parsed["text"]

        # Generate unique storage key and upload
        key = f"resumes/{user_id}/{uuid.uuid4().hex}-{file.filename}"
        file_url = upload_bytes_to_storage(key, content, file.content_type)

        # Insert into Supabase resumes table
        res = supabase.table("resumes").insert({
            "user_id": user_id,
            "file_url": file_url,
            "parsed_text": text
        }).select("*").execute()

        resume_id = res.data[0]["id"] if res and getattr(res, "data", None) else None

        # Compute job matches for ATS
        matches_info = compute_matches_for_resume(user_id, text)

        # Store AI role suggestions
        suggested_roles = suggest_roles_by_skills(skills)
        if suggested_roles:
            for role in suggested_roles:
                supabase.table("role_suggestions").insert({
                    "user_id": user_id,
                    "suggestion": role.get("role") if isinstance(role, dict) else role,
                    "confidence": role.get("confidence", None) if isinstance(role, dict) else None
                }).execute()

        return {
            "resume_id": resume_id,
            "file_url": file_url,
            "skills": skills,
            "matches": matches_info.get("matches"),
            "avg_score": matches_info.get("avg_score"),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


def list_resumes(user_id: str):
    """
    List all resumes of a user, ordered by creation date descending.
    """
    res = supabase.table("resumes").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return res.data if res and getattr(res, "data", None) else []


def get_resume(resume_id: str):
    """
    Retrieve a single resume by ID.
    """
    res = supabase.table("resumes").select("*").eq("id", resume_id).single().execute()
    return res.data if res and getattr(res, "data", None) else {}


def delete_resume(resume_id: str):
    """
    Delete a resume by ID.
    """
    try:
        # Fetch file URL for deletion from storage
        res = supabase.table("resumes").select("file_url").eq("id", resume_id).single().execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Resume not found")

        file_url = res.data.get("file_url")
        key = file_url.split("/storage/v1/object/public/")[1]  # extract storage key

        # Delete from Supabase storage
        supabase.storage.from_(key.split("/")[0]).remove(["/".join(key.split("/")[1:])])

        # Delete from DB
        supabase.table("resumes").delete().eq("id", resume_id).execute()

        return {"ok": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting resume: {str(e)}")
