def conversational_explanation(user_text, law, country):
    offence = law.get("offence", "a legal issue")
    section = law.get("law_section", "relevant law")
    punishment = law.get("punishment", "legal penalties")
    explanation = law.get("explanation", "")
    steps = law.get("next_steps", [])

    steps_text = ""
    if steps:
        steps_text = " Here is what you should do next: " + " → ".join(steps)

    return (
        f"I understand your situation. Based on what you described, this appears to be related to {offence}. "
        f"In {country.upper()}, such cases are handled under {section}. "
        f"{explanation} "
        f"If this offence is proven, the possible punishment may include {punishment}. "
        f"{steps_text} "
        f"If you want, you can ask me what to do first or how to report this legally."
    )