# backend/app/services/resume_service.py
import uuid
from fastapi import UploadFile, HTTPException
from app.supabase_client import supabase
from app.utils.storage_utils import upload_bytes_to_storage
from app.utils.nlp_utils import extract_text_and_skills
from app.services.ai_service import suggest_roles_by_skills
from app.services.matching_service import compute_matches_for_resume


async def upload_resume(file: UploadFile, user_id: str, job_desc: str = ""):
    """
    ✅ Upload a resume:
       - Stores file in Supabase Storage
       - Extracts text + skills (NLP)
       - Computes ATS job matches
       - Generates AI role suggestions
    """
    try:
        # Read file content
        content = await file.read()

        # Extract text and skills
        parsed = extract_text_and_skills(content, file.filename)
        skills = parsed.get("skills", [])
        text = parsed.get("text", "")

        # Upload file to Supabase storage
        key = f"resumes/{user_id}/{uuid.uuid4().hex}-{file.filename}"
        file_url = upload_bytes_to_storage(key, content, file.content_type)

        # Insert into resumes table
        res = supabase.table("resumes").insert({
            "user_id": user_id,
            "file_url": file_url,
            "parsed_text": text,
            "job_desc": job_desc or None,
        }).select("*").execute()

        resume_id = res.data[0]["id"] if res and getattr(res, "data", None) else None

        # Compute ATS matches
        matches_info = compute_matches_for_resume(user_id, text)

        # Store AI role suggestions
        suggested_roles = suggest_roles_by_skills(skills)
        if suggested_roles:
            rows = [
                {
                    "user_id": user_id,
                    "resume_id": resume_id,
                    "suggestion": role.get("role") if isinstance(role, dict) else role,
                    "confidence": role.get("confidence", None) if isinstance(role, dict) else None,
                }
                for role in suggested_roles
            ]
            supabase.table("role_suggestions").insert(rows).execute()

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
    ✅ List all resumes of a user (newest first).
    """
    try:
        res = (
            supabase.table("resumes")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return res.data if res and getattr(res, "data", None) else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching resumes: {str(e)}")


def get_resume(resume_id: str):
    """
    ✅ Retrieve a single resume by ID.
    """
    try:
        res = (
            supabase.table("resumes")
            .select("*")
            .eq("id", resume_id)
            .single()
            .execute()
        )
        return res.data if res and getattr(res, "data", None) else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving resume: {str(e)}")


def delete_resume(resume_id: str):
    """
    ✅ Delete a resume by ID (DB + Storage).
    """
    try:
        # Fetch file URL
        res = (
            supabase.table("resumes")
            .select("file_url")
            .eq("id", resume_id)
            .single()
            .execute()
        )
        if not res or not res.data:
            raise HTTPException(status_code=404, detail="Resume not found")

        file_url = res.data.get("file_url")
        if not file_url:
            raise HTTPException(status_code=400, detail="No file URL found for resume")

        # Extract storage bucket + path
        key = file_url.split("/storage/v1/object/public/")[1]
        bucket, path = key.split("/", 1)

        # Delete from Supabase storage
        supabase.storage.from_(bucket).remove([path])

        # Delete from DB
        supabase.table("resumes").delete().eq("id", resume_id).execute()

        return {"message": "Resume deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting resume: {str(e)}")
