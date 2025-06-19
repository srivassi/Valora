import requests
import pandas as pd
import time
import os

INTERVAL = "1d"
EXCHANGE = "iex"  # or binance, coinbase, etc.
SYMBOL = "AAPL"

TAAPI_BASE = "https://taapi.p.sulu.sh"
HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TAAPI_API_KEY')}"
}

def fetch_indicator(indicator, params={}):
    url = f"{BASE_URL}/{indicator}"
    params = {
        "secret": API_KEY,
        "exchange": "stocks",
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "backtrack": 90
    }
    default_params.update(params)
    response = requests.get(url, params=default_params)
    response.raise_for_status()
    return response.json()

def main():
    print(f"Fetching historical indicators for {SYMBOL}...")

    # Collect indicators
    rsi_data = fetch_indicator("rsi")
    macd_data = fetch_indicator("macd")
    ema50_data = fetch_indicator("ema", {"optInTimePeriod": 50})
    ema200_data = fetch_indicator("ema", {"optInTimePeriod": 200})
    stoch_data = fetch_indicator("stoch")
    bbands_data = fetch_indicator("bbands")
    obv_data = fetch_indicator("obv")
    price_data = fetch_indicator("price")  # To get closing prices

    all_data = []
    for i in range(90):
        try:
            entry = {
                "timestamp": rsi_data[i]["timestamp"],
                "close": price_data[i]["value"],
                "rsi": rsi_data[i]["value"],
                "macd": macd_data[i]["valueMACD"],
                "macd_signal": macd_data[i]["valueMACDSignal"],
                "ema_50": ema50_data[i]["value"],
                "ema_200": ema200_data[i]["value"],
                "stoch_k": stoch_data[i]["valueK"],
                "stoch_d": stoch_data[i]["valueD"],
                "bb_upper": bbands_data[i]["valueUpperBand"],
                "bb_middle": bbands_data[i]["valueMiddleBand"],
                "bb_lower": bbands_data[i]["valueLowerBand"],
                "obv": obv_data[i]["value"]
            }
            all_data.append(entry)
        except (KeyError, IndexError) as e:
            print(f"Skipping index {i}: {e}")

        # TAAPI rate limits: avoid being blocked
        time.sleep(3)

    df = pd.DataFrame(all_data)
    df.to_csv(f"{SYMBOL}_taapi_history.csv", index=False)
    print(f"✅ Saved {len(df)} rows to {SYMBOL}_taapi_history.csv")

if __name__ == "__main__":
    main()
