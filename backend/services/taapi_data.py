import requests
from backend.utils.ticker_loader import get_unique_tickers
import os
import json

TAAPI_BASE = "https://taapi.p.sulu.sh"
HEADERS = {
    "Accept": "application/json",
    "Authorization": os.getenv("TAAPI_API_KEY")
}

ENDPOINTS = [
    "/ema", "/macd", "/rsi", "/stoch", "/bbands", "/obv"
]
INTERVALS = ["1d", "1w"]

def fetch_taapi_data_for_ticker(ticker: str):
    results = {}
    for endpoint in ENDPOINTS:
        results[endpoint.strip("/")] = {}
        for interval in INTERVALS:
            url = f"{TAAPI_BASE}{endpoint}"
            params = {
                "exchange" : "stocks",
                "symbol" : ticker,
                "interval" : interval
            }
            response = requests.get(url, headers=HEADERS, params=params)
            if response.status_code == 200:
                results[endpoint.strip("/")] = response.json()
            else:
                results[endpoint.strip("/")] = {"error": response.text}
    return results

def fetch_all_tickers_taapi(save: bool=True):
    tickers = get_unique_tickers()
    full_results = {}
    for ticker in tickers:
        print(f"Fetching data for {ticker}")
        full_results[ticker] = fetch_taapi_data_for_ticker(ticker)

        if save:
            os.makedirs("data/taapi", exist_ok=True)
            with open(f"data/taapi/{ticker}.json", "w") as f:
                json.dump(full_results[ticker], f, indent=2)
    return full_results

if __name__ == "__main__":
    fetch_all_tickers_taapi()
