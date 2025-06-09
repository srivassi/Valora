import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def get_chat_response(prompt: str) -> str:
    """
    Sends a user prompt to Gemini and returns the model's response.
    """
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)
    return response.text
