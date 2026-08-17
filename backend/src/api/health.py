from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"message": "pong", "timestamp": datetime.now().isoformat()}

@router.get("/status")
async def status():
    return {
        "status": "online",
        "version": "1.0.0",
        "agents": 3,
        "uptime": "running"
    }
