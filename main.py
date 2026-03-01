@app.post("/chat")
def chat(request: ChatRequest):
    try:
        user_text = request.user_input.strip()
        country = request.country.strip().lower()
        role = request.user_role.strip().lower()

        if not user_text:
            return {"error": "User input is empty"}

        # -------- SAFE INTENT DETECTION --------
        intent = None
        if GEMINI_AVAILABLE:
            try:
                intent = extract_intent(user_text)
            except Exception:
                intent = None

        if not intent:
            intent = fallback_intent(user_text)

        # -------- SAFE LAW DATA LOADING --------
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        law_path = os.path.join(BASE_DIR, "law_data", f"{country}.json")

        if not os.path.exists(law_path):
            return {"error": f"Law data not found for country: {country}"}

        with open(law_path, "r", encoding="utf-8") as f:
            laws = json.load(f)

        law = laws.get(intent)

        if not law:
            return {
                "error": "Legal issue identified, but no matching law found",
                "detected_intent": intent
            }

        # -------- FINAL RESPONSE --------
        return {
            "issue": user_text,
            "country": country,
            "user_role": role,
            "detected_intent": intent,
            "law_section": law.get("law_section"),
            "offence": law.get("offence"),
            "punishment": law.get("punishment"),
            "explanation": law.get("explanation"),
            "next_steps": law.get("next_steps"),
            "note": "AI-based intent detection with safe fallback enabled"
        }

    except Exception as e:
        return {
            "error": "Internal server error",
            "debug": str(e)
        }