from fastapi import FastAPI

from agents.language_agent import detect_language
from agents.ml_intent_agent import MLIntentClassifier
from agents.law_agent import load_latest_law_data
from agents.response_agent import build_response
from agents.reasoning_agent import legal_reasoning
from agents.translation_agent import translate_to_english, translate_from_english

app = FastAPI(title="Global AI Legal Assistant")

intent_model = MLIntentClassifier()


@app.on_event("startup")
def startup_event():
    print("🔹 Initializing ML intent model...")
    intent_model.train()
    print("✅ ML intent model ready.")


@app.post("/chat")
def chat(
    user_input: str,
    country: str = "india",
    user_role: str = "citizen"
):
    detected_lang = detect_language(user_input)
    processed_input = translate_to_english(user_input, detected_lang)

    intent = intent_model.predict(processed_input)

    if intent == "unknown":
        return {
            "message": "Unable to identify the legal issue. Please provide more details."
        }

    laws, meta = load_latest_law_data(country)

    if intent not in laws:
        return {
            "message": "Law information not available for this issue."
        }

    law_info = laws[intent]
    reasoning = legal_reasoning(intent, processed_input, law_info)

    response = build_response(intent, law_info, meta, user_role)
    response["legal_reasoning"] = reasoning
    response["country"] = country
    response["user_role"] = user_role
    response["language_detected"] = detected_lang

    response = {
        key: translate_from_english(value, detected_lang)
        if isinstance(value, str) else value
        for key, value in response.items()
    }

    return response