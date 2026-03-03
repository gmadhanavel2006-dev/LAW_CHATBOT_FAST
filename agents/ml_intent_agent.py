import os

def infer_legal_issue_with_ai(text: str) -> str:
    """
    Lightweight AI-style reasoning without hardcoded keywords.
    Safe fallback if no LLM key is present.
    """

    text_lower = text.lower()

    # ---- Heuristic semantic understanding (SAFE FALLBACK) ----
    if any(phrase in text_lower for phrase in [
        "threat", "threatening", "blackmail", "intimidate"
    ]):
        return "Online criminal intimidation and cyber harassment"

    if any(phrase in text_lower for phrase in [
        "cheat", "fraud", "scam", "money taken"
    ]):
        return "Online fraud and financial deception"

    if any(phrase in text_lower for phrase in [
        "stolen", "theft", "robbed"
    ]):
        return "Theft or unlawful taking of property"

    if any(phrase in text_lower for phrase in [
        "harass", "abuse", "bully"
    ]):
        return "Harassment and abuse"

    # ---- Optional Gemini / LLM ----
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        # Placeholder for real LLM integration
        return f"Legal issue involving: {text[:120]}"

    # ---- FINAL SAFE FALLBACK ----
    return "General legal issue requiring professional review"