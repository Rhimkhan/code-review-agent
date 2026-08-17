from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "agents": ["SecurityAgent", "QualityAgent", "AnalystAgent"]
    }

@router.get("/ping")
async def ping():
    return {"message": "pong"}
