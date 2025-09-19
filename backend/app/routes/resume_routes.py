# backend/app/routes/resume_routes.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.resume_service import (
    upload_resume,
    list_resumes,
    get_resume,
    delete_resume,
)

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload")
async def upload_resume_route(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    job_desc: str = Form(None),
):
    """
    ✅ Upload a resume:
       - Stores file in Supabase
       - Parses resume
       - Generates AI job role suggestions (if job_desc provided)
    """
    try:
        result = await upload_resume(file, user_id, job_desc or "")
        return {
            "message": "Resume uploaded successfully",
            "data": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/list/{user_id}")
def list_user_resumes(user_id: str):
    """
    ✅ List all resumes for a given user.
    """
    try:
        return {"resumes": list_resumes(user_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching resumes: {str(e)}")


@router.get("/{resume_id}")
def get_single_resume(resume_id: str):
    """
    ✅ Retrieve a single resume by ID.
    """
    try:
        resume = get_resume(resume_id)
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        return resume
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving resume: {str(e)}")


@router.delete("/{resume_id}")
def delete_single_resume(resume_id: str):
    """
    ✅ Delete a resume by ID.
    """
    try:
        success = delete_resume(resume_id)
        if not success:
            raise HTTPException(status_code=404, detail="Resume not found")
        return {"message": "Resume deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting resume: {str(e)}")
