# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    auth_routes,
    resume_routes,
    job_routes,
    matching_routes,
    leaderboard_routes,
    ai_routes,
    admin_routes,
)

app = FastAPI(title="Resume Scanner + Job Matcher")

# ✅ Allow frontend origin (Vercel) + local dev
origins = [
    "https://ai-resume-and-job.vercel.app",  # your frontend
    "http://localhost:5173",                 # local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # change to ["*"] if you want all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routes
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Auth"])
app.include_router(resume_routes.router, prefix="/api/resume", tags=["Resume"])
app.include_router(job_routes.router, prefix="/api/job", tags=["Job"])
app.include_router(matching_routes.router, prefix="/api/match", tags=["Matching"])
app.include_router(leaderboard_routes.router, prefix="/api/leaderboard", tags=["Leaderboard"])
app.include_router(ai_routes.router, prefix="/api/ai", tags=["AI"])
app.include_router(admin_routes.router, prefix="/api", tags=["Admin"])  # /api/admin/*

# ✅ Simple health check
@app.get("/api/health")
def health():
    return {"ok": True}
