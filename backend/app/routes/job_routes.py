from fastapi import APIRouter, HTTPException
from app.models.schemas import JobCreate
from app.services.job_service import add_job, list_jobs, get_job_by_id, delete_job

router = APIRouter()

@router.post("/add")
def create_job(job: JobCreate):
    """Add a new job posting"""
    return add_job(job.dict())

@router.get("/list")
def list_all_jobs():
    """List all jobs"""
    return list_jobs()

@router.get("/{job_id}")
def get_job(job_id: str):
    """Get job by ID"""
    job = get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.delete("/{job_id}")
def delete_job_route(job_id: str):
    """Delete job by ID"""
    return delete_job(job_id)
