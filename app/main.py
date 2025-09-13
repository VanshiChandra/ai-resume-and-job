from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, resume_routes, job_routes, matching_routes, leaderboard_routes, ai_routes
from app.config import PORT

app = FastAPI(title="Resume Scanner + Job Matcher")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_routes.router, prefix="/api/auth", tags=["Auth"])
app.include_router(resume_routes.router, prefix="/api/resume", tags=["Resume"])
app.include_router(job_routes.router, prefix="/api/job", tags=["Job"])
app.include_router(matching_routes.router, prefix="/api/match", tags=["Matching"])
app.include_router(leaderboard_routes.router, prefix="/api/leaderboard", tags=["Leaderboard"])
app.include_router(ai_routes.router, prefix="/api/ai", tags=["AI"])

@app.get("/api/health")
def health():
    return {"ok": True}
