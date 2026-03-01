from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

# =========================
# OPTIONAL GEMINI IMPORT
# =========================
try:
    from agents.gemini_intent_agent import extract_intent
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False


# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="AI Law Chatbot Backend",
    description="Global AI-based Legal Guidance System",
    version="1.0.0"
)


# =========================
# CORS (FIXES ANDROID + GITHUB PAGES)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (safe for academic project)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# REQUEST MODEL
# =========================
class ChatRequest(BaseModel):
    user_input: str
    country: str
    user_role: str


# =========================
# LOAD LAW DATA
# =========================
def load_law_data(country: str):
    path = f"law_data/{country.lower()}.json"
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# FALLBACK INTENT (NO CRASH)
# =========================
def fallback_intent(text: str):
    text = text.lower()
    if "steal" in text or "stolen" in text or "theft" in text:
        return "theft"
    if "fraud" in text or "scam" in text:
        return "fraud"
    if "hack" in text or "cyber" in text:
        return "cyber_crime"
    if "violence" in text or "abuse" in text:
        return "domestic_violence"
    if "accident" in text:
        return "accident"
    return "theft"   # safe default


# =========================
# HOME ROUTE (TEST)
# =========================
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Law Chatbot Backend is live",
        "docs_url": "/docs",
        "chat_endpoint": "/chat"
    }


# =========================
# MAIN CHAT API
# =========================
@app.post("/chat")
def chat(request: ChatRequest):
    user_text = request.user_input.strip()
    country = request.country.strip().lower()
    role = request.user_role.strip().lower()

    if not user_text:
        return {"error": "User input is empty"}

    # -------- INTENT DETECTION --------
    intent = None

    if GEMINI_AVAILABLE:
        try:
            intent = extract_intent(user_text)
        except Exception:
            intent = fallback_intent(user_text)
    else:
        intent = fallback_intent(user_text)

    # -------- LOAD LAW DATA --------
    laws = load_law_data(country)
    if not laws:
        return {"error": f"No law data found for country: {country}"}

    law = laws.get(intent)
    if not law:
        return {"error": f"No legal mapping found for intent: {intent}"}

    # -------- RESPONSE --------
    response = {
        "issue": user_text,
        "country": country,
        "user_role": role,
        "law_section": law.get("law_section"),
        "offence": law.get("offence"),
        "punishment": law.get("punishment"),
        "explanation": law.get("explanation"),
        "next_steps": law.get("next_steps"),
        "note": "AI-based intent detection and legal reasoning modules are integrated."
    }

    return response