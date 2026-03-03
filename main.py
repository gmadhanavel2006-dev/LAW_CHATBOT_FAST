from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import traceback

from agents.translation_agent import (
    detect_language,
    translate_to_english,
    translate_from_english,
)
from agents.gemini_intent_agent import infer_legal_issue_with_ai
from agents.law_agent import load_law_data, match_relevant_laws
from agents.reasoning_agent import build_legal_reasoning
from agents.response_agent import generate_conversational_response

# =========================
# FASTAPI INITIALIZATION
# =========================

app = FastAPI(
    title="Global AI Legal Assistant",
    description="ChatGPT-style AI Lawyer Backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REQUEST / RESPONSE MODELS
# =========================

class ChatRequest(BaseModel):
    message: Optional[str] = ""
    country: Optional[str] = "india"
    role: Optional[str] = "citizen"


class ChatResponse(BaseModel):
    success: bool
    detected_language: str
    country: str
    issue_classification: str
    response: str
    laws_referenced: list
    error: Optional[str] = None


# =========================
# CHAT ENDPOINT
# =========================

@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        # ---- SAFE INPUT ----
        user_message = (payload.message or "").strip()
        if not user_message:
            return ChatResponse(
                success=True,
                detected_language="unknown",
                country=payload.country,
                issue_classification="unknown",
                response="Please describe your legal issue so I can help you.",
                laws_referenced=[],
            )

        country = (payload.country or "india").lower()
        role = (payload.role or "citizen").lower()

        # ---- LANGUAGE DETECTION ----
        detected_lang = detect_language(user_message)

        # ---- TRANSLATION TO ENGLISH ----
        if detected_lang != "en":
            english_text = translate_to_english(user_message, detected_lang)
        else:
            english_text = user_message

        # ---- AI ISSUE UNDERSTANDING ----
        try:
            issue_intent = infer_legal_issue_with_ai(english_text)
            if not issue_intent:
                raise ValueError("Empty AI intent")
        except Exception:
            issue_intent = "general legal issue requiring legal review"

        # ---- LOAD LAWS (NO HARDCODING) ----
        law_data = load_law_data(country)

        # ---- MATCH RELEVANT LAWS SAFELY ----
        matched_laws = match_relevant_laws(issue_intent, law_data)

        # ---- LEGAL REASONING ----
        reasoning = build_legal_reasoning(
            issue=issue_intent,
            matched_laws=matched_laws,
            country=country,
        )

        # ---- CONVERSATIONAL RESPONSE ----
        english_response = generate_conversational_response(
            issue=issue_intent,
            reasoning=reasoning,
            matched_laws=matched_laws,
            role=role,
            country=country,
        )

        # ---- TRANSLATE BACK ----
        if detected_lang != "en":
            final_response = translate_from_english(
                english_response, detected_lang
            )
        else:
            final_response = english_response

        # ---- SAFE OUTPUT ----
        return ChatResponse(
            success=True,
            detected_language=detected_lang,
            country=country,
            issue_classification=issue_intent,
            response=final_response,
            laws_referenced=[
                {
                    "offence_name": law.get("offence_name"),
                    "law_section": law.get("law_section"),
                }
                for law in matched_laws
                if isinstance(law, dict)
            ],
        )

    except Exception as e:
        traceback.print_exc()
        return ChatResponse(
            success=False,
            detected_language="unknown",
            country=payload.country or "unknown",
            issue_classification="unknown",
            response="Internal error occurred. Please try again.",
            laws_referenced=[],
            error=str(e),
        )


# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "Global AI Legal Assistant",
        "mode": "production-safe",
    }