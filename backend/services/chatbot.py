import os
import json
import pandas as pd
import google.generativeai as genai
import httpx
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.services.prompt_generator import generate_prompt, normalize_columns
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
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# === Company Metadata ===
company_list = load_company_names()
symbol_to_name = {item['symbol'].upper(): item['name'] for item in company_list}
name_to_symbol = {item['name'].lower(): item['symbol'].upper() for item in company_list}
valid_tickers = set(get_unique_tickers())
API_BASE = "http://localhost:8000"

# === Utils ===
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
        if word.lower() in name_to_symbol:
            return name_to_symbol[word.lower()]
    return None

async def fetch_company_data(ticker: str, data_type: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/company/{ticker}/{data_type}")
        return response.json()

def truncate_text(text: str, limit: int = 5000) -> str:
    return text[:limit] + "\n...[truncated]..." if len(text) > limit else text

def summarize_financials(data):
    rows = data if isinstance(data, list) else []
    summary = ""
    for row in rows[-3:]:
        year = row.get("Period.Ending", "Unknown")
        net_margin = row.get("net_margin", "N/A")
        roa = row.get("roa", "N/A")
        debt_equity = row.get("debt_equity", "N/A")
        summary += f"- {year}: Net Margin={net_margin}, ROA={roa}, Debt/Equity={debt_equity}\n"
    return summary or "No usable financial summary."

def save_chat_log(payload: dict, prompt: str, response: str):
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", "chat_log.jsonl")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            **payload,
            "prompt": prompt,
            "response": response
        }) + "\n")

def infer_prompt_type(message: str) -> str:
    msg = message.lower()
    if "ratio" in msg: return "ratios"
    if "anomal" in msg: return "anomalies"
    if "compare" in msg or "vs" in msg: return "compare"
    if "enhanced hypothesis" in msg or "signal" in msg: return "enhanced_hypothesis"
    if "hypothesis" in msg: return "hypothesis"
    if "trend" in msg: return "stock_trend"
    if "pros" in msg or "cons" in msg: return "pros_cons"
    if "score" in msg: return "score"
    if "overall" in msg: return "overall_analysis"
    if "financial" in msg: return "financials"
    if "taapi" in msg: return "taapi"
    if "feature" in msg: return "historical_features"
    if "stock" in msg: return "stock_data"
    return "ratios"

# === Request Schema ===
class ChatRequest(BaseModel):
    prompt_type: str = ""
    ticker: str
    persona: str = "general"
    question: str = ""

# === Main Endpoint ===
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        persona = request.persona.lower()
        question = request.question.strip()
        user_input = request.ticker.strip()

        if not question and not user_input:
            return {"reply": "❌ Please provide a valid question or company input."}

        prompt_type = request.prompt_type.lower().strip() if request.prompt_type else infer_prompt_type(question or user_input)

        if prompt_type == "compare":
            parts = [p.strip() for p in user_input.upper().split("vs")]
            if len(parts) != 2:
                return {"reply": "❌ Use format: 'AAPL vs MSFT'"}
            ticker1 = resolve_ticker(parts[0])
            ticker2 = resolve_ticker(parts[1])
            if not ticker1 or not ticker2:
                return {"reply": "❌ Invalid or unsupported tickers."}
            df = normalize_columns(pd.read_csv("data/useful_database/ratios.csv"))
            summary = df[df["ticker_symbol"].isin([ticker1, ticker2])].to_string(index=False)
            prompt = generate_prompt(prompt_type, question=question, ticker1=ticker1, ticker2=ticker2, comparison_summary=summary)

        else:
            ticker = resolve_ticker(extract_possible_ticker(user_input or question)) if prompt_type != "anomalies" else "IGNORED"
            print(f"🪙 Extracted Ticker: {ticker}")  # Debug for extraction
            if not ticker and prompt_type != "anomalies":
                return {"reply": f"❌ No valid ticker found in '{user_input or question}'."}

            if prompt_type == "ratios":
                df = normalize_columns(pd.read_csv("data/useful_database/ratios.csv"))
                summary = df[df["ticker_symbol"] == ticker].sort_values("period_ending", ascending=False).head(3).to_string(index=False)
                prompt = generate_prompt(prompt_type, question=question, persona=persona, ticker=ticker, ratios_summary=summary)

            elif prompt_type == "anomalies":
                df = normalize_columns(pd.read_csv("data/useful_database/anomalies.csv"))
                summary = df[df["anomaly"] == 1].head(5).to_string(index=False)
                prompt = generate_prompt(prompt_type, question=question, ticker=ticker, anomaly_summary=summary)

            elif prompt_type == "hypothesis":
                with open("data/useful_database/hypothesis_results.json") as f:
                    results = json.load(f)
                result = results[1] if "debt_equity" in results[1]["value_col"] else results[0]
                prompt = generate_prompt(prompt_type, question=question, persona=persona, ticker=ticker, year1="2020", year2="2023",
                                         mean1=result["mean_1"], mean2=result["mean_2"],
                                         t_statistic=result["t_statistic"], p_value=result["p_value"])

            elif prompt_type == "enhanced_hypothesis":
                path = f"backend/data/taapi_hyptest_results/{ticker}_hypothesis_results.json"
                if not os.path.exists(path):
                    return {"reply": f"❌ No enhanced hypothesis data for {ticker}."}
                with open(path) as f:
                    data_summary = json.load(f)
                prompt = generate_prompt(prompt_type, question=question, ticker=ticker, persona=persona, data_summary=json.dumps(data_summary, indent=2))

            elif prompt_type in {"financials", "taapi", "stock_data", "historical_features"}:
                data = await fetch_company_data(ticker, prompt_type)
                summary = summarize_financials(data) if prompt_type == "financials" else truncate_text(json.dumps(data, indent=2))
                prompt = generate_prompt(prompt_type, question=question, ticker=ticker, data_summary=summary)

            elif prompt_type == "overall_analysis":
                financials = await fetch_company_data(ticker, "financials")
                taapi = await fetch_company_data(ticker, "taapi")
                stock = await fetch_company_data(ticker, "stock_data")
                history = await fetch_company_data(ticker, "historical_features")
                prompt = generate_prompt(
                    prompt_type=prompt_type,
                    question=question,
                    persona=persona,
                    ticker=ticker,
                    ratios_summary=summarize_financials(financials),
                    taapi_summary=truncate_text(json.dumps(taapi, indent=2)),
                    stock_summary=truncate_text(json.dumps(stock, indent=2)),
                    historical_summary=truncate_text(json.dumps(history, indent=2))
                )

            elif prompt_type in {"pros_cons", "score"}:
                df = normalize_columns(pd.read_csv("data/useful_database/ratios.csv"))
                row = df[df["ticker_symbol"] == ticker].sort_values("period_ending", ascending=False).head(1)
                if row.empty:
                    return {"reply": f"❌ No recent ratio data for {ticker}."}
                summary = row.to_string(index=False)
                prompt = generate_prompt(prompt_type, question=question, ticker=ticker, persona=persona, data_summary=summary)

            elif prompt_type == "stock_trend":
                path = f"backend/data/useful_database/stock_data/{ticker}_historical_features.csv"
                if not os.path.exists(path):
                    return {"reply": f"❌ No stock trend data for {ticker}."}
                df = pd.read_csv(path)
                summary = df.tail(30).to_string(index=False)
                prompt = generate_prompt(prompt_type, question=question, ticker=ticker, data_summary=summary)

            else:
                return {"reply": f"❌ Unsupported prompt type: '{prompt_type}'."}

        print("📤 FINAL PROMPT TO GEMINI:\n", prompt)
        response = model.generate_content(prompt)

        save_chat_log({
            "prompt_type": prompt_type,
            "ticker": request.ticker,
            "persona": persona,
            "question": question
        }, prompt, response.text)

        return {"reply": response.text}

    except Exception as e:
        if "429" in str(e):
            return {"reply": "⚠️ Rate limit reached. Please wait and try again."}
        return {"reply": f"❌ Error: {str(e)}"}

# === Suggestions ===
@app.get("/chat/suggestions")
def get_suggested_queries():
    return {
        "suggestions": [
            {"label": "📊 Financial Ratios", "prompt_type": "ratios", "example": "AAPL"},
            {"label": "🚨 Anomaly Detection", "prompt_type": "anomalies", "example": "TSLA"},
            {"label": "🧪 Enhanced Hypothesis", "prompt_type": "enhanced_hypothesis", "example": "NVDA"},
            {"label": "🆚 Compare AAPL vs MSFT", "prompt_type": "compare", "example": "AAPL vs MSFT"},
            {"label": "📈 Stock Trend Summary", "prompt_type": "stock_trend", "example": "MSFT"},
            {"label": "📦 Overall Analysis", "prompt_type": "overall_analysis", "example": "META"},
            {"label": "👍 Pros & Cons Summary", "prompt_type": "pros_cons", "example": "GOOGL"},
            {"label": "🏅 Investment Score", "prompt_type": "score", "example": "AMZN"}
        ]
    }
