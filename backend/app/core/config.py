import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./cortex.db")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
APP_ENV: str = os.getenv("APP_ENV", "development")
