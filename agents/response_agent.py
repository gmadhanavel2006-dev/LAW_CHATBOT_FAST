def generate_conversational_response(issue, reasoning, matched_laws, role, country):
    if role == "lawyer":
        tone = "From a legal standpoint"
    else:
        tone = "In simple terms"

    response = f"{tone}, here is what is happening:\n\n"
    response += reasoning + "\n\n"

    for law in matched_laws:
        response += (
            f"• {law['offence_name']} ({law['law_section']}): "
            f"{law['explanation']}\n"
            f"  Possible punishment: {law['punishment']}\n"
            f"  Next steps: {law['next_steps']}\n\n"
        )

    if not matched_laws:
        response += "I recommend consulting a qualified lawyer for further guidance."

    return response.strip()