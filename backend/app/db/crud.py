from sqlalchemy.orm import Session
from app.db.models import Activity, User
from app.schemas.activity_schema import ActivityCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def get_user_by_username(db: Session, username: str) -> User:
    """Fetch a user by their username."""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, password: str) -> User:
    """Create a new user with a hashed password."""
    hashed_password = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_password(plain_password, hashed_password):
    """Verify a user's password against the stored hashed password."""
    return pwd_context.verify(plain_password, hashed_password)
