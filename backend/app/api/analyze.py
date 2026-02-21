from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.activity_schema import AnalysisResponse
from app.services.analysis_service import generate_analysis

router = APIRouter()


@router.get("/{user_id}", response_model=AnalysisResponse)
def analyze_learning(user_id: int, db: Session = Depends(get_db)):
    """Generate AI-powered learning insights for a user."""
    return generate_analysis(db, user_id)
