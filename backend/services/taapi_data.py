import requests
from backend.utils.ticker_loader import get_unique_tickers
from backend.services.stock_data import is_ticker_active, ticker_redirects
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

def is_ticker_taapi_valid(ticker: str) -> bool:
    url = f"{TAAPI_BASE}/rsi"
    params = {
        "exchange": "stocks",
        "symbol": ticker,
        "interval": "1d",
        "type": "stocks"
    }
    response = safe_api_call(url, headers=HEADERS, params=params, retries=1, timeout=10)
    return response is not None and response.status_code == 200


def safe_api_call(url, headers, params, retries=1, timeout=100):
    backoff = 2
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            return response
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print(f"[EXCEPTION] {type(e).__name__}: {e}")
            if attempt < retries:
                print(f"[RETRYING] Attempt {attempt + 1} of {retries} after error...")
                time.sleep(backoff)
                backoff *=2
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
                "interval" : interval,
                "type" : "stocks"
            }
            response = safe_api_call(url, headers=HEADERS, params=params, retries=2, timeout=30)

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

def fetch_all_tickers_taapi(tickers=None, save: bool=True):
    if tickers is None:
        tickers = get_unique_tickers()
    full_results = {}
    existing_tickers = []
    inactive_tickers = []
    taapi_failed_tickers = []

    for original_ticker in tickers:
        ticker = original_ticker.strip().upper()
        redirect = ticker_redirects.get(ticker, ticker)
        if redirect is None:
            print(f"[↯] {ticker} has no valid replacement. Skipping.")
            inactive_tickers.append(ticker)
            continue
        elif redirect != ticker:
            print(f"[↪] Redirecting {ticker} → {redirect}")
            ticker = redirect

        if not is_ticker_taapi_valid(ticker):
            print(f"[✘] {ticker} appears inactive or delisted. Skipping.")
            inactive_tickers.append(original_ticker)
            continue

        filepath = f"../../data/taapi/{ticker}.json"
        if os.path.exists(filepath):
            print(f"[↻] Skipping {ticker}, TAAPI data already exists.")
            existing_tickers.append(ticker)
            continue

        print(f"Fetching TAAPI data for {ticker}")
        data = fetch_taapi_data_for_ticker(ticker)

        if any("error" in val for val in data.values()):
            print(f"[ERROR] TAAPI issue for {ticker} → {data}")
            taapi_failed_tickers.append(ticker)
            continue  # skip this one, move on

        full_results[original_ticker] = data

        if save:
            os.makedirs("../../data/taapi", exist_ok=True)
            with open(f"../../data/taapi/{original_ticker}.json", "w") as f:
                json.dump(data, f, indent=2)

        time.sleep(1)

    print("\n[SUMMARY]")
    print(f"✓ New tickers fetched: {len(full_results)}")
    print(f"↻ Existing tickers skipped: {len(existing_tickers)}")
    print(f"✘ Inactive/delisted tickers skipped: {len(inactive_tickers)}")
    print(f"⚠ TAAPI failed tickers skipped: {len(taapi_failed_tickers)}")


    if inactive_tickers:
        with open("../../data/taapi/skipped_inactive_tickers.txt", "w") as f:
            for t in inactive_tickers:
                f.write(t + "\n")
        print(
            f"\n[INFO] Logged {len(inactive_tickers)} inactive/delisted tickers to 'data/taapi/skipped_inactive_tickers.txt'.")

    if taapi_failed_tickers:
        with open("../../data/taapi/skipped_tickers.txt", "w") as f:
            for t in taapi_failed_tickers:
                f.write(t + "\n")
        print(f"\n[INFO] Logged {len(taapi_failed_tickers)} TAAPI failed tickers to 'data/taapi/skipped_tickers.txt'.")

    print("\nInactive/delisted tickers:")
    print(inactive_tickers)
    print(f"Total inactive/delisted skipped: {len(inactive_tickers)}")

    print("\nTAAPI failed tickers:")
    print(taapi_failed_tickers)
    print(f"Total TAAPI failed skipped: {len(taapi_failed_tickers)}")

    return full_results, taapi_failed_tickers

def load_skipped_tickers():
    path = "../../data/taapi/skipped_tickers.txt"
    if os.path.exists(path):
        with open(path, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

if __name__ == "__main__":
    _, taapi_failed_tickers = fetch_all_tickers_taapi()

    if taapi_failed_tickers:
        print(f"\nRetrying {len(taapi_failed_tickers)} tickers that failed TAAPI call...")
        time.sleep(3)  # short pause before retry

        _, skipped_again = fetch_all_tickers_taapi(tickers=taapi_failed_tickers)

        if skipped_again:
            retry_path = "../../data/taapi/skipped_tickers_retry.txt"
            with open(retry_path, "w") as f:
                f.write(f"# Retry attempt on {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                for t in skipped_again:
                    f.write(t + "\n")
            print(f"[INFO] Still skipped {len(skipped_again)} tickers after retry. Logged to '{retry_path}'.")
        else:
            print("✅ All skipped tickers succeeded on retry.")
    else:
        print("✅ No TAAPI failed tickers to retry.")

