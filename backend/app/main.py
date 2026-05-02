from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import track, analyze, plan, auth
from app.db.database import engine
from app.db import models
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

# Create tables on startup (use Alembic for production migrations)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cortex Study Tracker API",
    description="AI-powered study activity tracker and planner",
    version="0.1.0",
)
load_dotenv()

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: ( {"detail": "Rate limit exceeded"}, 429 ))
app.add_middleware(SlowAPIMiddleware)

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if origin.strip() and origin.strip().lower() != "null"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"chrome-extension://.*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(track.router, prefix="/api/track", tags=["Track"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["Analyze"])
app.include_router(plan.router, prefix="/api/plan", tags=["Plan"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Cortex API is running"}


# JWT settings (in production, use env vars and strong secrets)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")


# Example: protect a route (apply to routers/endpoints as needed)
# @app.get("/api/protected")
# def protected_route(user_id: int = Depends(get_current_user)):
#     return {"user_id": user_id}
