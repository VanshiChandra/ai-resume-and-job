# backend/app/models/schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional


class RegisterRequest(BaseModel):
    name: str  # ✅ required
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ResumeUploadResponse(BaseModel):
    resume_id: str
    file_url: Optional[str] = None
    skills: List[str]
    avg_score: Optional[float] = None


class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: Optional[List[str]] = None  # ✅ avoids mutable default []


class MatchResult(BaseModel):
    job_id: str
    job_title: str
    score: float
    missing_skills: List[str]
    matched_skills: List[str]
