import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI()

# Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only, restrict in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini
api_key= os.getenv('GEMINI_API_KEY')
genai.configure(api_key)
print(os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel("gemini-2.5-flash")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")

    try:
        response = model.generate_content(user_message)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
