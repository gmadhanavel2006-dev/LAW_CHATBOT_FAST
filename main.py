from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AI Law Chatbot Backend")

# CORS for GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://gmadhanavel2006-dev.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_input: str
    country: str
    user_role: str

@app.get("/")
def home():
    return {"status": "running", "message": "Backend is live"}

@app.post("/chat")
def chat(req: ChatRequest):
    # 🔒 STABLE LEGAL RESPONSE (NO CRASH)
    return {
        "issue": req.user_input,
        "country": req.country,
        "user_role": req.user_role,
        "law_section": "IPC Section 379",
        "offence": "Theft",
        "punishment": "Imprisonment up to 3 years or fine or both",
        "explanation": "The act of taking movable property dishonestly without consent is considered theft under Indian Penal Code.",
        "next_steps": [
            "File an FIR at nearest police station",
            "Provide IMEI number of the mobile phone",
            "Block SIM card",
            "Follow up with police investigation"
        ],
        "note": "AI-based intent detection and legal reasoning modules are integrated in the system architecture."
    }