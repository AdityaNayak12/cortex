from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.activity_schema import StudyPlanResponse
from app.services.plan_service import create_study_plan
from app.main import get_current_user

router = APIRouter()


@router.get("/me", response_model=StudyPlanResponse)
def get_study_plan(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    """Generate a personalized daily study plan for the authenticated user."""
    return create_study_plan(db, user_id)
