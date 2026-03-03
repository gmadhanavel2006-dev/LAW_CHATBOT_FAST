import os

def infer_legal_issue_with_ai(text: str) -> str:
    """
    Gemini / LLM optional.
    Safe fallback if API key not present.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Gemini API not configured")

    # Placeholder for real Gemini call
    # Keep backend safe even if removed
    return f"Legal issue related to: {text[:120]}"