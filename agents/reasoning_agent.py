def build_legal_reasoning(issue: str, matched_laws: list, country: str) -> str:
    if not matched_laws:
        return f"The issue appears legally relevant in {country}, but no exact law match was found."

    return (
        f"The issue involves legal concerns in {country}. "
        f"Based on the nature of the problem, certain laws may apply "
        f"to protect rights and define consequences."
    )