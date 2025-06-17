import os
import json
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

from services.prompt_generator import (
    generate_ratio_prompt,
    generate_anomaly_prompt,
    generate_hypothesis_prompt,
)

# Load environment variables
load_dotenv()

# Configure Gemini with API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Initialize model
model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")

# Initialize FastAPI
app = FastAPI()

# Allow CORS for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request format
class ChatRequest(BaseModel):
    prompt_type: str  # "ratios", "anomalies", or "hypothesis"
    ticker: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        ticker = request.ticker.upper()
        prompt_type = request.prompt_type.lower()

        if prompt_type == "ratios":
            df_ratios = pd.read_csv("data/ratios.csv")
            prompt = generate_ratio_prompt(ticker, df_ratios)

        elif prompt_type == "anomalies":
            df_anomalies = pd.read_csv("data/anomalies.csv")
            prompt = generate_anomaly_prompt(df_anomalies)

        elif prompt_type == "hypothesis":
            with open("data/hypothesis_results.json") as f:
                results = json.load(f)
            result = results[1] if "debt_equity" in results[1]["value_col"] else results[0]
            prompt = generate_hypothesis_prompt(result, ticker=ticker, year1="2020", year2="2023")

        else:
            return {"reply": f"Invalid prompt type: {prompt_type}"}

        response = model.generate_content(prompt)
        return {"reply": response.text}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
