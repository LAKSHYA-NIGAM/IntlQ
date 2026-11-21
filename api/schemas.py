"""
Request / Response Schemas
Pydantic models for API validation.
"""

from pydantic import BaseModel, Field, field_validator


class StartInterviewRequest(BaseModel):
    """Request to start a new interview session."""
    candidate_name: str = Field(default="Anonymous", max_length=100)
    role_id: str = Field(..., min_length=1)
    difficulty: str | None = Field(default=None)
    question_count: int = Field(default=5, ge=1, le=20)

    @field_validator("candidate_name")
    @classmethod
    def sanitize_candidate_name(cls, v: str) -> str:
        stripped = v.strip()
        return stripped if stripped else "Anonymous"

    @field_validator("role_id")
    @classmethod
    def validate_role_id(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("role_id cannot be blank or whitespace")
        return stripped


class SubmitAnswerRequest(BaseModel):
    """Request to submit an answer for evaluation."""
    session_id: int = Field(..., ge=1)
    question_id: str = Field(..., min_length=1)
    answer_text: str = Field(..., min_length=1)

    @field_validator("question_id")
    @classmethod
    def validate_question_id(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("question_id cannot be blank or whitespace")
        return stripped

    @field_validator("answer_text")
    @classmethod
    def validate_answer_text(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("answer_text cannot be empty or only whitespace")
        return stripped
