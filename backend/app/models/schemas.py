from pydantic import BaseModel, EmailStr
from typing import List, Optional

class RegisterRequest(BaseModel):
    name: Optional[str]
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ResumeUploadResponse(BaseModel):
    resume_id: str
    file_url: Optional[str]
    skills: List[str]
    avg_score: Optional[float]

class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: Optional[List[str]] = []

class MatchResult(BaseModel):
    job_id: str
    job_title: str
    score: float
    missing_skills: List[str]
    matched_skills: List[str]
