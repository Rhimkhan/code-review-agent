from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
import traceback

from src.agents.orchestrator import Orchestrator
from src.middleware.rate_limiter import limiter
from src.auth.routes import router as auth_router

app = FastAPI(
    title="Code Review Agent API",
    description="AI-powered multi-agent code review system",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

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
async def health():
    return {"status": "healthy"}


@app.post("/api/review/code")
@limiter.limit("5/minute")
async def review_code(request: Request, body: CodeReviewRequest):
    try:
        review = await orchestrator.review_code(body.code, body.filename)

        return {
            "status": "success",
            "review": review
        }

    except Exception as e:
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(e),
                "type": type(e).__name__
            },
        )


@app.get("/api/review/demo")
async def demo_review():
    sample_code = """
def hello(name):
    print("Hello", name)
"""

    try:
        review = await orchestrator.review_code(sample_code, "demo.py")

        return {
            "status": "success",
            "review": review
        }

    except Exception as e:
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error": str(e),
                "type": type(e).__name__
            },
        )


@app.post("/api/review/pr")
@limiter.limit("3/minute")
async def review_pr(request: Request, body: PRReviewRequest):
    return {
        "status": "success",
        "message": "PR review not implemented yet"
    }