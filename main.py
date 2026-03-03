from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

# ------------------------
# FastAPI APP (REQUIRED)
# ------------------------
app = FastAPI(title="AI Law Chatbot")

# ------------------------
# CORS (for GitHub Pages)
# ------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later you can lock this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Request Model
# ------------------------
class ChatRequest(BaseModel):
    user_input: str
    country: str = "india"
    user_role: str = "citizen"

# ------------------------
# Health Check (IMPORTANT)
# ------------------------
@app.get("/")
def home():
    return {"status": "OK", "message": "AI Law Chatbot running"}

# ------------------------
# Load Law Data
# ------------------------
def load_laws(country: str):
    path = f"law_data/{country.lower()}.json"
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ------------------------
# Simple Intent Mapping (TEMP)
# ------------------------
def basic_intent_detect(text: str):
    t = text.lower()
    if "blackmail" in t:
        return "blackmail"
    if "stolen" in t or "theft" in t:
        return "theft"
    if "harass" in t:
        return "harassment"
    return "unknown"

# ------------------------
# Chat Endpoint
# ------------------------
@app.post("/chat")
def chat(req: ChatRequest):
    laws = load_laws(req.country)
    intent = basic_intent_detect(req.user_input)

    for law in laws:
        if law.get("intent") == intent:
            return {
                "issue": req.user_input,
                "country": req.country,
                "user_role": req.user_role,
                "detected_intent": intent,
                "law_section": law.get("section"),
                "offence": law.get("offence"),
                "punishment": law.get("punishment"),
                "explanation": law.get("explanation"),
                "next_steps": law.get("next_steps"),
                "note": "AI legal guidance (stable base)"
            }

    return {
        "issue": req.user_input,
        "detected_intent": intent,
        "message": "No matching law found. Please provide more details."
    }