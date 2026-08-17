import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from src.agents.orchestrator import Orchestrator
from src.middleware.rate_limiter import limiter

load_dotenv()

app = FastAPI(title="Code Review Agent", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0", "agents": 3}

@app.post("/api/review/code")
async def review_code(request: dict):
    code = request.get("code", "")
    filename = request.get("filename", "code.py")
    result = await orchestrator.review_code(code=code, filename=filename)
    return {"status": "success", "review": result}

@app.get("/api/review/demo")
async def demo_review():
    demo_code = """
import sqlite3
SECRET_KEY = "hardcoded_secret"

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = '" + username + "'")
    return cursor.fetchone()

def process(a, b, c, d, e, f, g):
    try:
        return a+b+c+d+e+f+g
    except:
        pass
"""
    result = await orchestrator.review_code(code=demo_code, filename="demo.py")
    return {"status": "success", "review": result}
