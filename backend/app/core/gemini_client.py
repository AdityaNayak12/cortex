import logging

from google import genai
from app.core.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

# gemini-2.0-flash-lite has its own free-tier quota separate from gemini-2.0-flash
MODEL = "gemini-2.5-flash"

_client = None


class GeminiAPIError(Exception):
    """Raised when the Gemini API call fails."""


def get_client() -> genai.Client:
    """Lazily initialise and return the Gemini client."""
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError(
                "Cannot initialise Gemini client: GEMINI_API_KEY is not set."
            )
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def generate_text(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    try:
        response = get_client().models.generate_content(model=MODEL, contents=prompt)
        return response.text
    except Exception as exc:
        logger.error("Gemini API call failed: %s", exc, exc_info=True)
        raise GeminiAPIError(f"Gemini API call failed: {exc}") from exc

