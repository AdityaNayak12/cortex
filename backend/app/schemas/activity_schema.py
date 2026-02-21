from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# ── Request schema ────────────────────────────────────────────────────────────

class ActivityCreate(BaseModel):
    user_id: int
    subject: str
    topic: Optional[str] = None
    duration_minutes: float
    performance_score: Optional[float] = None  # 0–100
    notes: Optional[str] = None


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
