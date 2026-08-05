from pydantic import BaseModel, Field
from typing import Optional

class CodeReviewRequest(BaseModel):
    code: str = Field(..., min_length=1)
    filename: str = Field(default="code.py")
    language: Optional[str] = None
