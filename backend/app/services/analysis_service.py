from sqlalchemy.orm import Session
from app.db.crud import get_activities_by_user
from app.core.gemini_client import generate_text, GeminiAPIError
from app.schemas.activity_schema import AnalysisResponse


def generate_analysis(db: Session, user_id: int) -> AnalysisResponse:
    """Build a Gemini prompt from the user's activity history and return insights."""
    activities = get_activities_by_user(db, user_id)

    if not activities:
        return AnalysisResponse(user_id=user_id, insights="No activity data found yet.")

    summary_lines = [
        f"- {a.subject} / {a.topic}: {a.duration_minutes} min, score {a.performance_score}"
        for a in activities
    ]
    summary = "\n".join(summary_lines)

    prompt = (
        f"You are an expert learning coach. Analyse the following study sessions for user {user_id} "
        f"and provide clear, actionable insights on strengths, weaknesses, and patterns:\n{summary}"
    )

    try:
        insights = generate_text(prompt)
    except GeminiAPIError:
        insights = "Unable to generate insights. Please try again later."

    return AnalysisResponse(user_id=user_id, insights=insights)

