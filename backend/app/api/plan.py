from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.activity_schema import StudyPlanResponse
from app.services.plan_service import create_study_plan

router = APIRouter()


@router.get("/{user_id}", response_model=StudyPlanResponse)
def get_study_plan(user_id: int, db: Session = Depends(get_db)):
    """Generate a personalized daily study plan for a user."""
    return create_study_plan(db, user_id)
