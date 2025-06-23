import os
import json
import pandas as pd
import google.generativeai as genai
import httpx
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.services.prompt_generator import (
    generate_ratio_prompt,
    generate_anomaly_prompt,
    generate_enhanced_hypothesis_prompt,
    generate_hypothesis_prompt,
    generate_stock_trend_prompt,
    generate_comparison_prompt
)

from backend.services.company_data_store import load_company_names
from backend.utils.ticker_loader import get_unique_tickers
from backend.services.api.company_data_api import router as company_data_router


# === Gemini Setup ===
load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY is missing")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")

# === FastAPI Setup ===
app = FastAPI()
app.include_router(company_data_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Load Company Data ===
company_list = load_company_names()
symbol_to_name = {item['symbol'].upper(): item['name'] for item in company_list}
name_to_symbol = {item['name'].lower(): item['symbol'].upper() for item in company_list}
valid_tickers = set(get_unique_tickers())
API_BASE = "http://localhost:8000"

# === Utility Functions ===
def resolve_ticker(user_input: str) -> str:
    upper = user_input.upper()
    lower = user_input.lower()
    if upper in valid_tickers:
        return upper
    if lower in name_to_symbol and name_to_symbol[lower] in valid_tickers:
        return name_to_symbol[lower]
    for name, symbol in name_to_symbol.items():
        if lower in name and symbol in valid_tickers:
            return symbol
    return None

def extract_possible_ticker(text: str) -> str:
    for word in reversed(text.strip().split()):
        candidate = word.strip(",.?!").upper()
        if candidate in valid_tickers:
            return candidate
        lower = word.lower()
        if lower in name_to_symbol:
            return name_to_symbol[lower]
    return text.strip()

async def fetch_company_data(ticker: str, data_type: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/company/{ticker}/{data_type}")
        return response.json()

# === Request Model ===
class ChatRequest(BaseModel):
    prompt_type: str
    ticker: str

# === /chat Endpoint ===
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        prompt_type = request.prompt_type.lower()
        user_input = request.ticker.strip()

        # Resolve ticker unless prompt_type is anomalies
        ticker = resolve_ticker(extract_possible_ticker(user_input)) if prompt_type != "anomalies" else "IGNORED"

        if not ticker and prompt_type != "anomalies":
            return {"reply": f"No data found for '{user_input}'."}

        # === Prompt Generation ===
        if prompt_type == "ratios":
            df = pd.read_csv("data/useful_database/ratios.csv")
            prompt = generate_ratio_prompt(ticker, df)

        elif prompt_type == "anomalies":
            df = pd.read_csv("data/useful_database/anomalies.csv")
            prompt = generate_anomaly_prompt(df)

        elif prompt_type == "enhanced_hypothesis":
            prompt = generate_enhanced_hypothesis_prompt(ticker)

        elif prompt_type == "hypothesis":
            with open("data/useful_database/hypothesis_results.json") as f:
                results = json.load(f)
            result = results[1] if "debt_equity" in results[1]["value_col"] else results[0]
            prompt = generate_hypothesis_prompt(result, ticker, year1="2020", year2="2023")

        elif prompt_type == "stock_trend":
            prompt = generate_stock_trend_prompt(ticker)

        elif prompt_type == "compare":
            df = pd.read_csv("data/useful_database/ratios.csv")
            prompt = generate_comparison_prompt("AAPL", "MSFT", df)

        elif prompt_type in {"financials", "taapi", "stock_data", "historical_features"}:
            data = await fetch_company_data(ticker, prompt_type)
            prompt = f"Analyze the following {prompt_type} data for {ticker}:\n{data}"

        elif prompt_type == "overall_analysis":
            financials = await fetch_company_data(ticker, "financials")
            taapi = await fetch_company_data(ticker, "taapi")
            stock = await fetch_company_data(ticker, "stock_data")
            history = await fetch_company_data(ticker, "historical_features")
            prompt = (
                f"Provide an overall financial analysis for {ticker} using the following:\n"
                f"- Financials: {financials}\n"
                f"- TAAPI: {taapi}\n"
                f"- Stock Data: {stock}\n"
                f"- Historical Features: {history}\n"
            )

        else:
            return {"reply": f"❌ Invalid prompt type: '{prompt_type}'"}

        response = model.generate_content(prompt)
        return {"reply": response.text}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}

# === /chat/suggestions Endpoint ===
@app.get("/chat/suggestions")
def get_suggested_queries():
    return {
        "suggestions": [
            {"label": "📊 Financial Ratios", "prompt_type": "ratios", "example": "AAPL"},
            {"label": "🚨 Anomaly Detection", "prompt_type": "anomalies", "example": "AAPL"},
            {"label": "🧪 Enhanced Hypothesis", "prompt_type": "enhanced_hypothesis", "example": "AAPL"},
            {"label": "🆚 Compare AAPL vs MSFT", "prompt_type": "compare", "example": "AAPL vs MSFT"},
            {"label": "📈 Stock Trend Summary", "prompt_type": "stock_trend", "example": "AAPL"},
            {"label": "📦 Overall Analysis", "prompt_type": "overall_analysis", "example": "AAPL"},
        ]
    }
