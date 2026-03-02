from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

# ===============================
# OPTIONAL GEMINI AI IMPORT
# ===============================
try:
    from agents.gemini_intent_agent import extract_intent
    GEMINI_ENABLED = True
except Exception:
    GEMINI_ENABLED = False


# ===============================
# FASTAPI APP
# ===============================
app = FastAPI(
    title="AI Law Chatbot Backend",
    description="Global AI-based Legal Guidance System",
    version="1.0.0"
)

# ===============================
# CORS (Web + Android Safe)
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# REQUEST MODEL
# ===============================
class ChatRequest(BaseModel):
    user_input: str
    country: str
    user_role: str


# ===============================
# COUNTRY NORMALIZATION
# ===============================
def normalize_country(country: str):
    country = country.strip().lower()

    country_map = {
        "india": "india",
        "bharat": "india",

        "usa": "usa",
        "us": "usa",
        "united states": "usa",
        "united states of america": "usa",

        "uk": "uk",
        "united kingdom": "uk",
        "england": "uk",
        "britain": "uk"
    }

    return country_map.get(country, country)


# ===============================
# FALLBACK INTENT (NO CRASH)
# ===============================
def fallback_intent(text: str):
    text = text.lower()

    if "steal" in text or "stolen" in text or "theft" in text:
        return "theft"
    if "fraud" in text or "scam" in text or "cheat" in text:
        return "fraud"
    if "hack" in text or "cyber" in text:
        return "cyber_crime"
    if "violence" in text or "abuse" in text:
        return "domestic_violence"
    if "accident" in text or "crash" in text:
        return "accident"

    return "theft"  # safe default


# ===============================
# HOME ROUTE
# ===============================
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Law Chatbot Backend is live",
        "gemini_enabled": GEMINI_ENABLED
    }


# ===============================
# MAIN CHAT ENDPOINT
# ===============================
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        user_text = request.user_input.strip()
        role = request.user_role.strip().lower()
        country = normalize_country(request.country)

        if not user_text:
            return {"error": "User input is empty"}

        # -------- INTENT DETECTION --------
        intent = None

        if GEMINI_ENABLED:
            try:
                intent = extract_intent(user_text)
            except Exception:
                intent = None

        if not intent:
            intent = fallback_intent(user_text)

        # -------- LOAD LAW DATA (ABSOLUTE PATH) --------
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        law_path = os.path.join(BASE_DIR, "law_data", f"{country}.json")

        if not os.path.exists(law_path):
            return {
                "error": "Law data not found",
                "country_received": request.country,
                "country_used": country
            }

        with open(law_path, "r", encoding="utf-8") as f:
            laws = json.load(f)

        law = laws.get(intent)

        if not law:
            return {
                "error": "No matching law found",
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
            "note": "AI-powered legal guidance using Gemini with safe fallback"
        }

    except Exception as e:
        return {
            "error": "Internal server error",
            "debug": str(e)
        }