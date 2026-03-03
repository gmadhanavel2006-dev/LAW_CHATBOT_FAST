import os
import requests
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment variables")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-pro:generateContent?key=" + GEMINI_API_KEY
)

def understand_issue(user_input: str, country: str, user_role: str):
    """
    Uses Gemini AI to understand the legal issue semantically.
    Returns structured intent usable by law engine.
    """

    prompt = f"""
You are an AI legal assistant.

User country: {country}
User role: {user_role}

User message:
\"\"\"{user_input}\"\"\"

Your task:
1. Identify the legal issue
2. Explain it in simple terms
3. Suggest applicable law sections
4. Suggest next legal steps

Respond ONLY in valid JSON with keys:
issue_summary, legal_domain, explanation, next_steps
"""

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(
        GEMINI_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30
    )

    response.raise_for_status()
    result = response.json()

    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    except Exception:
        return {
            "issue_summary": user_input,
            "legal_domain": "general law",
            "explanation": "Unable to fully parse AI response.",
            "next_steps": "Consult a legal professional."
        }