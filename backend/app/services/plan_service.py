from sqlalchemy.orm import Session
from app.db.crud import get_activities_by_user
from app.core.gemini_client import generate_text
from app.schemas.activity_schema import StudyPlanResponse


def create_study_plan(db: Session, user_id: int) -> StudyPlanResponse:
    """Use recent activity history to ask Gemini to produce a daily study plan."""
    activities = get_activities_by_user(db, user_id)

    if not activities:
        return StudyPlanResponse(user_id=user_id, plan="Please log some study sessions first.")

    summary_lines = [
        f"- {a.subject} / {a.topic}: {a.duration_minutes} min, score {a.performance_score}"
        for a in activities[-10:]  # Use the 10 most recent sessions
    ]
    summary = "\n".join(summary_lines)

    prompt = (
        f"Based on the following recent study sessions for user {user_id}, "
        f"create a detailed, realistic daily study plan for tomorrow. "
        f"Prioritise weak areas and balance the workload:\n{summary}"
    )

    plan = generate_text(prompt)
    return StudyPlanResponse(user_id=user_id, plan=plan)
