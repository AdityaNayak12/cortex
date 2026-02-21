from sqlalchemy.orm import Session
from app.db.crud import create_activity
from app.schemas.activity_schema import ActivityCreate, ActivityResponse


def process_activity(db: Session, payload: ActivityCreate) -> ActivityResponse:
    """Validate and persist an incoming activity event."""
    activity = create_activity(db, payload)
    return ActivityResponse.model_validate(activity)
