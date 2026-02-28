from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
# REQUEST MODEL (IMPORTANT)
# -------------------------
class ChatRequest(BaseModel):
    user_input: str
    country: str = "india"
    user_role: str = "citizen"


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
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ML MODEL
# -------------------------
intent_model = MLIntentClassifier()


# -------------------------
# STARTUP
# -------------------------
@app.on_event("startup")
def startup_event():
    print("🔹 Initializing ML intent model...")
    intent_model.train()
    print("✅ ML intent model ready.")


# -------------------------
# HOME
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
# CHAT API (JSON BODY)
# -------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.user_input
    country = request.country.lower()
    user_role = request.user_role.lower()

    # 1️⃣ Detect language
    detected_lang = detect_language(user_input)

    # 2️⃣ Translate to English
    processed_input = translate_to_english(user_input, detected_lang)

    # 3️⃣ Predict intent
    intent = intent_model.predict(processed_input)

    if intent == "unknown":
        return {
            "message": "Unable to identify the legal issue. Please provide more details."
        }

    # 4️⃣ Load law data
    laws, meta = load_latest_law_data(country)

    if intent not in laws:
        return {
            "message": "Law information not available for this issue."
        }

    law_info = laws[intent]

    # 5️⃣ Reasoning
    reasoning = legal_reasoning(intent, processed_input, law_info)

    # 6️⃣ Response
    response = build_response(
        intent=intent,
        law_info=law_info,
        meta=meta,
        user_role=user_role
    )

    response.update({
        "legal_reasoning": reasoning,
        "country": country,
        "user_role": user_role,
        "language_detected": detected_lang
    })

    # 7️⃣ Translate back
    final_response = {}
    for k, v in response.items():
        final_response[k] = (
            translate_from_english(v, detected_lang)
            if isinstance(v, str) else v
        )

    return final_response