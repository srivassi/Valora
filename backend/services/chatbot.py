import os
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load variables from .env
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Enable CORS for all origins (dev only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini with API key from .env
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Choose supported model
model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")

# Define request schema
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = model.generate_content(request.message)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
