from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
# REQUEST MODEL
# -------------------------
class ChatRequest(BaseModel):
    user_input: str
    country: str = "india"
    user_role: str = "citizen"


# -------------------------
# APP INIT
# -------------------------
app = FastAPI(title="Global AI Law Chatbot")

# -------------------------
# CORS — FINAL FIX
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://gmadhanavel2006-dev.github.io"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

# -------------------------
# ML MODEL
# -------------------------
intent_model = MLIntentClassifier()

@app.on_event("startup")
def startup():
    intent_model.train()


# -------------------------
# ROOT
# -------------------------
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Law Chatbot Backend is Live",
        "chat_endpoint": "/chat"
    }


# -------------------------
# CHAT ENDPOINT
# -------------------------
@app.post("/chat")
async def chat(request: ChatRequest):
    user_input = request.user_input
    country = request.country.lower()
    user_role = request.user_role.lower()

    detected_lang = detect_language(user_input)
    processed_input = translate_to_english(user_input, detected_lang)

    intent = intent_model.predict(processed_input)
    if intent == "unknown":
        return {"message": "Unable to identify the legal issue."}

    laws, meta = load_latest_law_data(country)
    if intent not in laws:
        return {"message": "Law data not found for this issue."}

    law_info = laws[intent]
    reasoning = legal_reasoning(intent, processed_input, law_info)

    response = build_response(
        intent=intent,
        law_info=law_info,
        meta=meta,
        user_role=user_role
    )

    response["legal_reasoning"] = reasoning
    response["language_detected"] = detected_lang

    final = {}
    for k, v in response.items():
        final[k] = (
            translate_from_english(v, detected_lang)
            if isinstance(v, str) else v
        )

    return JSONResponse(content=final)