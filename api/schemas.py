"""
Request / Response Schemas
Pydantic models for API validation.
"""

from pydantic import BaseModel, Field


class StartInterviewRequest(BaseModel):
    """Request to start a new interview session."""
    candidate_name: str = Field(default="Anonymous", max_length=100)
    role_id: str = Field(..., min_length=1)
    difficulty: str | None = Field(default=None)
    question_count: int = Field(default=5, ge=1, le=20)


class SubmitAnswerRequest(BaseModel):
    """Request to submit an answer for evaluation."""
    session_id: int = Field(...)
    question_id: str = Field(..., min_length=1)
    answer_text: str = Field(..., min_length=1)
