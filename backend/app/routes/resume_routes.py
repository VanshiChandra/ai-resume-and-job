from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.resume_service import process_resume, list_resumes, get_resume, delete_resume

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload")
async def upload_resume_route(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    job_desc: str = Form(None)
):
    """
    Upload a resume, parse it, store in Supabase, and generate AI role suggestions.
    """
    try:
        result = await process_resume(file, user_id, job_desc or "")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list/{user_id}")
def list_user_resumes(user_id: str):
    """
    List all resumes of a specific user.
    """
    return list_resumes(user_id)


@router.get("/{resume_id}")
def get_single_resume(resume_id: str):
    """
    Retrieve a single resume by ID.
    """
    return get_resume(resume_id)


@router.delete("/{resume_id}")
def delete_single_resume(resume_id: str):
    """
    Delete a resume by ID.
    """
    return delete_resume(resume_id)
