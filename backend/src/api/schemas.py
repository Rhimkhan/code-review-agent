from pydantic import BaseModel, Field
from typing import Optional

class CodeReviewRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Source code to review")
    filename: str = Field(default="code.py", description="Filename with extension")
    language: Optional[str] = Field(default=None, description="Programming language")

class FindingResponse(BaseModel):
    type: str
    subtype: str
    line: int
    severity: str
    message: str
    suggestion: str

class ReviewResponse(BaseModel):
    status: str
    total_findings: int
    summary: str
    findings: list
    severity_counts: dict
