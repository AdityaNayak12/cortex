from google import genai
from app.core.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

# gemini-2.0-flash-lite has its own free-tier quota separate from gemini-2.0-flash
MODEL = "gemini-2.5-flash"


def generate_text(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text
