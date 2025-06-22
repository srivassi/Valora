import os
import json
import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import httpx

from services.prompt_generator import (
    generate_ratio_prompt,
    generate_anomaly_prompt,
    generate_hypothesis_prompt,
)
from services.company_data_store import load_company_names
from utils.ticker_loader import get_unique_tickers
from .api.company_data_api import router as company_data_router

app = FastAPI()
app.include_router(company_data_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"Using Gemini API key: {api_key}")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.5-flash-preview-05-20")

# Build mappings
company_list = load_company_names()
symbol_to_name = {item['symbol'].upper(): item['name'] for item in company_list}
name_to_symbol = {item['name'].lower(): item['symbol'].upper() for item in company_list}
valid_tickers = set(get_unique_tickers())

# Define request format
class ChatRequest(BaseModel):
    prompt_type: str  # "ratios", "anomalies", or "hypothesis"
    ticker: str

API_BASE = "http://localhost:8000"

async def fetch_company_data(ticker, data_type):
    async with httpx.AsyncClient() as client:
        url = f"{API_BASE}/company/{ticker}/{data_type}"
        resp = await client.get(url)
        return resp.json()


def resolve_ticker(user_input):
    input_upper = user_input.upper()
    input_lower = user_input.lower()
    print(f"resolve_ticker: user_input='{user_input}', input_upper='{input_upper}'")
    if input_upper in valid_tickers:
        print(f"Matched ticker: {input_upper}")
        return input_upper
    if input_lower in name_to_symbol:
        ticker = name_to_symbol[input_lower]
        if ticker in valid_tickers:
            print(f"Matched company name: {input_lower} -> {ticker}")
            return ticker
    for name, symbol in name_to_symbol.items():
        if input_lower in name:
            if symbol in valid_tickers:
                print(f"Partial match: {input_lower} in {name} -> {symbol}")
                return symbol
    print("No match found")
    return None

def extract_possible_ticker(user_input):
    # Split by spaces, check each word from the end
    words = user_input.strip().split()
    for word in reversed(words):
        candidate = word.strip(",.?!").upper()
        if candidate in valid_tickers:
            return candidate
        candidate_lower = word.strip(",.?!").lower()
        if candidate_lower in name_to_symbol:
            return name_to_symbol[candidate_lower]
    return user_input.strip()

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        user_input = request.ticker.strip()
        prompt_type = request.prompt_type.lower()
        # Extract possible ticker/company name from user input
        extracted = extract_possible_ticker(user_input)
        ticker = resolve_ticker(extracted)
        if not ticker:
            return {"reply": f"No data found for '{user_input}'."}

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
        elif prompt_type in ["financials", "taapi", "stock_data", "historical_features"]:
            data = await fetch_company_data(ticker, prompt_type)
            prompt = f"Analyze the following {prompt_type} for {ticker}: {data}"

        elif prompt_type == "overall_analysis":
            # Fetch all data types
            financials = await fetch_company_data(ticker, "financials")
            taapi = await fetch_company_data(ticker, "taapi")
            stock_data = await fetch_company_data(ticker, "stock_data")
            historical_features = await fetch_company_data(ticker, "historical_features")
            prompt = (
                f"Provide an overall financial analysis for {ticker} using the following data:\n"
                f"Financials: {financials}\n"
                f"TAAPI: {taapi}\n"
                f"Stock Data: {stock_data}\n"
                f"Historical Features: {historical_features}\n"
            )

        else:
            return {"reply": f"Invalid prompt type: {prompt_type}"}

        response = model.generate_content(prompt)
        return {"reply": response.text}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}
