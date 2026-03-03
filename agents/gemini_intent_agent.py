import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def detect_intent_with_gemini(user_text: str) -> str:
    if not GEMINI_API_KEY:
        return "unknown"

    try:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            "models/gemini-1.5-pro:generateContent"
            f"?key={GEMINI_API_KEY}"
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""
Identify the legal issue category from this user message.
Return ONLY one word like:
theft, blackmail, harassment, assault, fraud, cybercrime, domestic_violence.

User message:
{user_text}
"""
                        }
                    ]
                }
            ]
        }

        res = requests.post(url, json=payload, timeout=15)

        if res.status_code != 200:
            return "unknown"

        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip().lower()

    except Exception:
        return "unknown"