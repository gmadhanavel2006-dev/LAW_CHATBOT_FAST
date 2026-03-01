from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.language_agent import detect_language
from agents.ml_intent_agent import MLIntentClassifier
from agents.law_agent import load_latest_law_data
from agents.response_agent import build_response
from agents.reasoning_agent import legal_reasoning
from agents.translation_agent import translate_to_english, translate_from_english


class ChatRequest(BaseModel):
    user_input: str
    country: str = "india"
    user_role: str = "citizen"


app = FastAPI(title="AI Law Chatbot")

# 🔴 IMPORTANT: exact GitHub Pages origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://gmadhanavel2006-dev.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)

intent_model = MLIntentClassifier()

@app.on_event("startup")
def startup():
    intent_model.train()


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/chat")
def chat(req: ChatRequest):
    detected_lang = detect_language(req.user_input)
    text_en = translate_to_english(req.user_input, detected_lang)

    intent = intent_model.predict(text_en)
    laws, meta = load_latest_law_data(req.country.lower())

    if intent not in laws:
        return {"message": "Law not found for this issue."}

    law_info = laws[intent]
    reasoning = legal_reasoning(intent, text_en, law_info)

    response = build_response(
        intent=intent,
        law_info=law_info,
        meta=meta,
        user_role=req.user_role
    )

    response["legal_reasoning"] = reasoning

    final = {}
    for k, v in response.items():
        final[k] = translate_from_english(v, detected_lang) if isinstance(v, str) else v

    return final