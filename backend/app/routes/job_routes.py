from fastapi import APIRouter, HTTPException
from app.models.schemas import JobCreate
from app.services.job_service import add_job, list_jobs, get_job_by_id, delete_job

router = APIRouter(prefix="/job", tags=["Job"])

# ============================
# Add a new job
# ============================
@router.post("/add")
def create_job(job: JobCreate):
    try:
        new_job = add_job(job.dict())
        return {"success": True, "data": new_job}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add job: {str(e)}")

# ============================
# List all jobs
# ============================
@router.get("/list")
def list_all_jobs():
    try:
        jobs = list_jobs()
        return {"success": True, "data": jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list jobs: {str(e)}")

# ============================
# Get job by ID
# ============================
@router.get("/{job_id}")
def get_job(job_id: str):
    try:
        job = get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"success": True, "data": job}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch job: {str(e)}")

# ============================
# Delete job by ID
# ============================
@router.delete("/{job_id}")
def delete_job_route(job_id: str):
    try:
        result = delete_job(job_id)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete job: {str(e)}")
