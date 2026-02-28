def legal_reasoning(issue: str, user_input: str, law_info: dict):
    reasons = []

    text = user_input.lower()

    if issue == "theft":
        if any(word in text for word in ["stolen", "steal", "திருட", "चोरी"]):
            reasons.append("Movable property appears to be taken")
        if any(word in text for word in ["without permission", "without consent", "திருட"]):
            reasons.append("Property taken without consent")
        reasons.append("Indicates dishonest intention")

    elif issue == "fraud":
        if any(word in text for word in ["cheated", "scam", "மோசடி", "धोखा"]):
            reasons.append("User was deceived intentionally")
        reasons.append("Dishonest inducement detected")

    return {
        "reasoning": reasons,
        "conclusion": f"{law_info.get('section')} is applicable based on the identified facts."
    }