import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def extract_intent(user_text: str) -> str:
    """
    Uses Gemini to understand the user's legal intent.
    Returns a normalized intent string.
    """

    # 🔒 Fallback if API key not set
    if not GEMINI_API_KEY:
        return "unknown"

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""
You are a legal intent classifier.
From the user text, return ONLY one intent keyword from this list:
theft, fraud, domestic_violence, cyber_crime, accident, unknown.

User text:
{user_text}
"""
                    }
                ]
            }
        ]
    }

    response = requests.post(
        f"{url}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload,
        timeout=10
    )

    data = response.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]

    return text.strip().lower()