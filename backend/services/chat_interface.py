import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv(find_dotenv())

# Get your Gemini API key from the environment
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

#Fail fast if the key is missing
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY is missing. Make sure it's defined in your .env file.")

# Configure Gemini with the API key
genai.configure(api_key=api_key)

# Load the Gemini model
model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")

# Function to send prompt and return Gemini response
def get_chat_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
