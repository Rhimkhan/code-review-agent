from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
import os

load_dotenv()

from src.agents.orchestrator import Orchestrator
from src.middleware.rate_limiter import limiter
from src.auth.routes import router as auth_router

app = FastAPI(
    title="Code Review Agent API",
    description="AI-powered multi-agent code review system",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")

orchestrator = Orchestrator()


class CodeReviewRequest(BaseModel):
    code: str
    filename: str = "code.py"


class PRReviewRequest(BaseModel):
    repo: str
    pr_number: int


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.post("/api/review/code")
@limiter.limit("5/minute")
async def review_code(request: Request, body: CodeReviewRequest):
    try:
        if not body.code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")
        result = await orchestrator.review_code(body.code, body.filename)
        return {"status": "success", "review": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "error": str(e)})


@app.post("/api/review/pr")
@limiter.limit("3/minute")
async def review_pr(request: Request, body: PRReviewRequest):
    try:
        from src.tools.github_tools import GitHubTools
        github = GitHubTools()
        files = await github.get_pr_files(body.repo, body.pr_number)
        if not files:
            raise HTTPException(status_code=404, detail="No files found in PR")
        all_reviews = []
        for file in files:
            if file.contents:
                review = await orchestrator.review_code(file.contents, file.filename)
                all_reviews.append(review)
        total_findings = sum(r['total_findings'] for r in all_reviews)
        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for review in all_reviews:
            for severity, count in review.get('severity_counts', {}).items():
                severity_counts[severity] += count
        return {
            "status": "success",
            "review": {
                "pr_number": body.pr_number,
                "repo": body.repo,
                "files_reviewed": len(all_reviews),
                "total_findings": total_findings,
                "severity_counts": severity_counts,
                "file_reviews": all_reviews
            }
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "error": str(e)})


@app.get("/api/review/demo")
async def demo_review():
    sample_code = """
def login(username, password):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    password = "admin123"
    return query
"""
    result = await orchestrator.review_code(sample_code, "auth.py")
    return {"status": "success", "review": result}