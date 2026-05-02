from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional


# ── Request schema ────────────────────────────────────────────────────────────

class ActivityCreate(BaseModel):
    user_id: int
    subject: str
    topic: Optional[str] = None
    duration_minutes: float
    performance_score: Optional[float] = None  # 0–100
    notes: Optional[str] = None

    @field_validator("subject")
    @classmethod
    def subject_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("subject must not be empty")
        return v.strip()

    @field_validator("duration_minutes")
    @classmethod
    def duration_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("duration_minutes must be greater than 0")
        return v

    @field_validator("performance_score")
    @classmethod
    def score_must_be_in_range(cls, v: float | None) -> float | None:
        if v is not None and (v < 0 or v > 100):
            raise ValueError("performance_score must be between 0 and 100")
        return v


# ── Response schemas ──────────────────────────────────────────────────────────

class ActivityResponse(BaseModel):
    id: int
    user_id: int
    subject: str
    topic: Optional[str]
    duration_minutes: float
    performance_score: Optional[float]
    notes: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalysisResponse(BaseModel):
    user_id: int
    insights: str


class StudyPlanResponse(BaseModel):
    user_id: int
    plan: str


# ── User schemas ─────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
