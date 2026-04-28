import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./cortex.db")
APP_ENV: str = os.getenv("APP_ENV", "development")

_gemini_key = os.getenv("GEMINI_API_KEY", "")
if not _gemini_key or not _gemini_key.strip():
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Add it to your .env file or export it as an environment variable.\n"
        "  Example: GEMINI_API_KEY=your-api-key-here"
    )
GEMINI_API_KEY: str = _gemini_key.strip()
