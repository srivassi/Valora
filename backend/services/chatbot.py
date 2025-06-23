import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# === Load Gemini API Key ===
load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY is missing")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")

# === Setup FastAPI ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Import prompt generators ===
from backend.services.prompt_generator import (
    generate_ratio_prompt,
    generate_anomaly_prompt,
    generate_enhanced_hypothesis_prompt,
    generate_stock_trend_prompt
)

# === Company Name to Ticker Map ===
def get_ticker_from_name(company_name: str) -> str:
    name_to_ticker = {
        "Apple": "AAPL",
        "Amazon": "AMZN",
        "Meta": "META",
        "Microsoft": "MSFT",
        "Google": "GOOGL"
    }
    return name_to_ticker.get(company_name.title(), "")

# === Request schema ===
class FreePrompt(BaseModel):
    prompt_type: str
    company_name: str

# === Chat endpoint ===
@app.post("/chat")
async def chat(request: FreePrompt):
    ticker = get_ticker_from_name(request.company_name)

    if not ticker:
        return {"reply": f"❌ Company '{request.company_name}' not found."}

    try:
        if request.prompt_type == "ratios":
            df_ratios = pd.read_csv("backend/data/useful_database/ratios.csv")
            prompt = generate_ratio_prompt(ticker, df_ratios)

        elif request.prompt_type == "anomaly":
            df_anomalies = pd.read_csv("backend/data/useful_database/anomalies.csv")
            prompt = generate_anomaly_prompt(df_anomalies)

        elif request.prompt_type == "enhanced_hypothesis":
            prompt = generate_enhanced_hypothesis_prompt(ticker)

        elif request.prompt_type == "stock_trend":
            prompt = generate_stock_trend_prompt(ticker)
        elif request.prompt_type == "compare":
            df_ratios = pd.read_csv("backend/data/useful_database/ratios.csv")
            # TEMP: hardcoded pair
            prompt = generate_comparison_prompt("AAPL", "MSFT", df_ratios)
        else:
            prompt = f"❌ Unknown prompt type: {request.prompt_type}"

        response = model.generate_content(prompt)
        return {"reply": response.text}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
