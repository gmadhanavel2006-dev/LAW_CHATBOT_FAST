from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(
    title="AI Law Chatbot Backend",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_input: str
    country: str
    user_role: str


def fallback_intent(text: str):
    text = text.lower()
    if "steal" in text or "stolen" in text:
        return "theft"
    if "fraud" in text or "scam" in text:
        return "fraud"
    if "hack" in text or "cyber":
        return "cyber_crime"
    if "violence" in text or "abuse":
        return "domestic_violence"
    if "accident" in text:
        return "accident"
    return "theft"


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Law Chatbot Backend is live"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        intent = fallback_intent(request.user_input)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        law_path = os.path.join(BASE_DIR, "law_data", f"{request.country.lower()}.json")

        if not os.path.exists(law_path):
            return {"error": "Law data not found"}

        with open(law_path, "r", encoding="utf-8") as f:
            laws = json.load(f)

        law = laws.get(intent)

        if not law:
            return {"error": "No matching law found"}

        return {
            "issue": request.user_input,
            "country": request.country,
            "intent": intent,
            "law_section": law["law_section"],
            "offence": law["offence"],
            "punishment": law["punishment"],
            "explanation": law["explanation"],
            "next_steps": law["next_steps"]
        }

    except Exception as e:
        return {"error": "Server error", "debug": str(e)}