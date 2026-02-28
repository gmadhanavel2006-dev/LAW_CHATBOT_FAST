from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agents.language_agent import detect_language
from agents.ml_intent_agent import MLIntentClassifier
from agents.law_agent import load_latest_law_data
from agents.response_agent import build_response
from agents.reasoning_agent import legal_reasoning
from agents.translation_agent import (
    translate_to_english,
    translate_from_english
)

# -------------------------
# APP INITIALIZATION
# -------------------------
app = FastAPI(
    title="Global AI Law Chatbot",
    description="AI-powered legal assistant for global users",
    version="1.0"
)

# -------------------------
# CORS CONFIGURATION
# (MANDATORY FOR WEBSITE)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (safe for academic project)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ML MODEL INITIALIZATION
# -------------------------
intent_model = MLIntentClassifier()


# -------------------------
# STARTUP EVENT
# -------------------------
@app.on_event("startup")
def startup_event():
    print("🔹 Initializing ML intent model...")
    intent_model.train()
    print("✅ ML intent model ready.")


# -------------------------
# HOME ROUTE (HEALTH CHECK)
# -------------------------
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Law Chatbot Backend is Live",
        "docs_url": "/docs",
        "chat_endpoint": "/chat"
    }


# -------------------------
# MAIN CHAT API
# -------------------------
@app.post("/chat")
def chat(
    user_input: str,
    country: str = "india",
    user_role: str = "citizen"
):
    # 1️⃣ Detect language
    detected_lang = detect_language(user_input)

    # 2️⃣ Translate to English (processing language)
    processed_input = translate_to_english(user_input, detected_lang)

    # 3️⃣ Predict legal intent using ML
    intent = intent_model.predict(processed_input)

    if intent == "unknown":
        return {
            "message": "Unable to identify the legal issue. Please provide more details."
        }

    # 4️⃣ Load country-specific law data
    laws, meta = load_latest_law_data(country)

    if intent not in laws:
        return {
            "message": "Law information not available for this issue."
        }

    law_info = laws[intent]

    # 5️⃣ Legal reasoning engine
    reasoning = legal_reasoning(intent, processed_input, law_info)

    # 6️⃣ Build role-based response
    response = build_response(
        intent=intent,
        law_info=law_info,
        meta=meta,
        user_role=user_role
    )

    response["legal_reasoning"] = reasoning
    response["country"] = country
    response["user_role"] = user_role
    response["language_detected"] = detected_lang

    # 7️⃣ Translate response back to user language
    translated_response = {}
    for key, value in response.items():
        if isinstance(value, str):
            translated_response[key] = translate_from_english(value, detected_lang)
        else:
            translated_response[key] = value

    return translated_response