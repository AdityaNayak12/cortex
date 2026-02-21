from sqlalchemy.orm import Session
from app.db.models import Activity
from app.schemas.activity_schema import ActivityCreate


def create_activity(db: Session, payload: ActivityCreate) -> Activity:
    """Insert a new activity record into the database."""
    activity = Activity(**payload.model_dump())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def get_activities_by_user(db: Session, user_id: int) -> list[Activity]:
    """Fetch all activity records for a specific user."""
    return db.query(Activity).filter(Activity.user_id == user_id).all()
