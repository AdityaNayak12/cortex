from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.activity_schema import AnalysisResponse
from app.services.analysis_service import generate_analysis
from app.main import get_current_user

router = APIRouter()


@router.get("/me", response_model=AnalysisResponse)
def analyze_learning(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    """Generate AI-powered learning insights for the authenticated user."""
    return generate_analysis(db, user_id)
