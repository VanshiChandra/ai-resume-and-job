from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.resume_service import process_resume, list_resumes, get_resume, delete_resume

router = APIRouter()

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), user_id: str = Form(...), job_desc: str = Form(None)):
    try:
        res = await process_resume(file, user_id, job_desc or "")
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{user_id}")
def resume_list(user_id: str):
    return list_resumes(user_id)

@router.get("/{resume_id}")
def resume_get(resume_id: str):
    return get_resume(resume_id)

@router.delete("/{resume_id}")
def resume_delete(resume_id: str):
    return delete_resume(resume_id)
