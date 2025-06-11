import requests
from backend.utils.ticker_loader import get_unique_tickers
import os
import json
import time

TAAPI_BASE = "https://taapi.p.sulu.sh"
HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TAAPI_API_KEY')}"
}
print(os.getenv("TAAPI_API_KEY"))

ENDPOINTS = [
    "/ema", "/macd", "/rsi", "/stoch", "/bbands", "/obv"
]
INTERVALS = ["1d", "1w"]

def safe_api_call(url, headers, params, retries=1, timeout=10):
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            return response
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print(f"[EXCEPTION] {type(e).__name__}: {e}")
            if attempt < retries:
                print(f"[RETRYING] Attempt {attempt + 1} of {retries} after error...")
                time.sleep(2)
            else:
                return None  # fail gracefully

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
            response = safe_api_call(url, headers=HEADERS, params=params, retries=1, timeout=10)

            if response is None:
                results[endpoint.strip("/")]["error"] = {
                    "status": "timeout",
                    "message": "Request timed out or connection failed"
                }
                return results  # Early exit
            if response.status_code == 200:
                results[endpoint.strip("/")][interval] = response.json()
            else:
                print(f"[ERROR] {ticker} | {endpoint.strip("/")} | {interval} => {response.status_code}: {response.text}")
                results[endpoint.strip("/")]["error"] = {
                    "status": response.status_code,
                    "message": response.text
                }
                return results
    return results

def fetch_all_tickers_taapi(save: bool=True):
    tickers = get_unique_tickers()
    full_results = {}
    for ticker in tickers:
        print(f"Fetching data for {ticker}")
        data = fetch_taapi_data_for_ticker(ticker)

        if any("error" in val for val in data.values()):
            print("[ABORTING] Error occurred; stopping to avoid wasting credits.")
            break

        full_results[ticker] = data

        if save:
            os.makedirs("data/taapi", exist_ok=True)
            with open(f"data/taapi/{ticker}.json", "w") as f:
                json.dump(data, f, indent=2)
    return full_results

if __name__ == "__main__":
    fetch_all_tickers_taapi()
