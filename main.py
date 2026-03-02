from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

# ===============================
# FASTAPI APP
# ===============================
app = FastAPI(
    title="AI Law Chatbot Backend",
    description="Global AI-based Legal Guidance System",
    version="1.0.0"
)

# ===============================
# CORS (Web + Android safe)
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
# COUNTRY NORMALIZATION (KEY FIX)
# ===============================
def normalize_country(country: str):
    country = country.strip().lower()

    country_map = {
        # India
        "india": "india",
        "bharat": "india",

        # USA
        "usa": "usa",
        "us": "usa",
        "united states": "usa",
        "united states of america": "usa",

        # UK
        "uk": "uk",
        "united kingdom": "uk",
        "england": "uk",
        "britain": "uk"
    }

    return country_map.get(country, country)


# ===============================
# FALLBACK INTENT (STABLE)
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
        "message": "AI Law Chatbot Backend is live"
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

        # -------- INTENT --------
        intent = fallback_intent(user_text)

        # -------- LOAD LAW DATA (ABSOLUTE PATH FIX) --------
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
                "error": "No matching law found for detected intent",
                "detected_intent": intent
            }

        # -------- RESPONSE --------
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
            "note": "Global AI legal guidance system with safe fallback"
        }

    except Exception as e:
        return {
            "error": "Internal server error",
            "debug": str(e)
        }