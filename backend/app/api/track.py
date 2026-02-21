from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.activity_schema import ActivityCreate, ActivityResponse
from app.services.tracker_service import process_activity

router = APIRouter()


@router.post("/", response_model=ActivityResponse)
def track_activity(payload: ActivityCreate, db: Session = Depends(get_db)):
    """Receive and persist a study activity event."""
    return process_activity(db, payload)
