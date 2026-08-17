from fastapi import Header, HTTPException
from typing import Optional

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Optional API key verification for future auth"""
    return True

async def get_request_context(
    user_agent: Optional[str] = Header(None),
    x_forwarded_for: Optional[str] = Header(None)
):
    return {
        "user_agent": user_agent,
        "ip": x_forwarded_for or "unknown"
    }
