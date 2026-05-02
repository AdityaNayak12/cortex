from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)


class Activity(Base):
    """Represents a single study activity session logged by the user."""

    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    subject = Column(String(255), nullable=False)
    topic = Column(String(255), nullable=True)
    duration_minutes = Column(Float, nullable=False)
    performance_score = Column(Float, nullable=True)  # 0–100
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
