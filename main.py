from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents.gemini_intent_agent import GeminiLegalReasoner

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

reasoner = GeminiLegalReasoner()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()

    user_input = data.get("user_input", "")
    country = data.get("country", "india")
    user_role = data.get("user_role", "citizen")

    analysis = reasoner.analyze(user_input, country)

    return {
        "issue": analysis["legal_issue"],
        "country": country,
        "user_role": user_role,
        "offences_identified": analysis["offences"],
        "applicable_laws": analysis["applicable_laws"],
        "explanation": analysis["citizen_explanation"],
        "next_steps": analysis["immediate_steps"],
        "note": "AI-generated legal guidance. Not a substitute for a lawyer."
    }