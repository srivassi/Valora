import requests
import os

TAAPI_BASE = "https://taapi.p.sulu.sh"
HEADERS = {
    "Accept": "application/json",
    "Authorization": os.getenv("TAAPI_API_KEY")
}

def get_bbands(ticker: str):
    return requests.get(
        f"{TAAPI_BASE}/bbands",
        headers=HEADERS,
        params={"exchange": "stocks", "symbol": ticker, "interval": "1d"}
    ).json()