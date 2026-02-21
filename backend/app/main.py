from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import track, analyze, plan
from app.db.database import engine
from app.db import models

# Create tables on startup (use Alembic for production migrations)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cortex Study Tracker API",
    description="AI-powered study activity tracker and planner",
    version="0.1.0",
)

# Allow all origins so the dashboard (Live Server :5500) and
# Chrome extension can call the API without CORS errors.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(track.router, prefix="/api/track", tags=["Track"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["Analyze"])
app.include_router(plan.router, prefix="/api/plan", tags=["Plan"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Cortex API is running"}
