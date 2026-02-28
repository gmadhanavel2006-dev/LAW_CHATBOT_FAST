def build_response(issue, law_info, meta_info, user_role="citizen"):
    base_response = {
        "issue_identified": issue,
        "law_name": law_info.get("law_name"),
        "section": law_info.get("section"),
        "severity": law_info.get("severity"),
        "law_version": meta_info.get("version"),
        "law_year": meta_info.get("year"),
        "last_updated": meta_info.get("last_updated"),
        "disclaimer": "This is for informational purposes only and not legal advice."
    }

    # Role-based customization
    if user_role == "citizen":
        base_response.update({
            "explanation": law_info.get("explanation"),
            "what_you_should_do": [
                "Go to the nearest police station",
                "File an FIR or complaint",
                "Preserve all evidence",
                "Consult a lawyer if required"
            ],
            "legal_flow": law_info.get("legal_flow")
        })

    elif user_role == "lawyer":
        base_response.update({
            "legal_conditions": law_info.get("conditions"),
            "procedure": law_info.get("legal_flow"),
            "punishment": law_info.get("punishment"),
            "note": "This information is intended for professional reference."
        })

    elif user_role == "accused":
        base_response.update({
            "important_rights": [
                "Right to remain silent",
                "Right to legal counsel",
                "Right against self-incrimination",
                "Right to fair trial"
            ],
            "legal_advice": "It is strongly recommended to consult a qualified lawyer immediately.",
            "punishment": law_info.get("punishment")
        })

    else:
        base_response["message"] = "Invalid user role selected."

    return base_response