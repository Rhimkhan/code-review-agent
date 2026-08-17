from fastapi import Header
from typing import Optional

async def get_request_context(
    user_agent: Optional[str] = Header(None),
    x_forwarded_for: Optional[str] = Header(None)
):
    return {
        "user_agent": user_agent,
        "ip": x_forwarded_for or "unknown"
    }
