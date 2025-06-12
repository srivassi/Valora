import os
import time

import yfinance as yf
import datetime
import pandas as pd
from backend.utils.ticker_loader import get_unique_tickers

DATA_DIR = "../../data/stock_data"

ticker_redirects = {
    "FB": "META", "PCLN": "BKNG", "YHOO": None, "CELG": "BMY",
    "MON": "BAYN.DE", "COL": "RTX", "DPS": "KDP", "LLTC": "ADI",
    "DISCA": "WBD", "DISCK": "WBD", "SNI": "WBD", "FBHS": "MAS",
    "KORS": "CPRI", "SYMC": "GEN", "VIAB": "PARA", "ATVI": "MSFT",
    "ALXN": "AZN", "WFM": "AMZN", "ADS": "SYF", "CTXS": None,
    "BCR": "BDX", "BHI": "HAL", "LLL": "LHX", "HRS": "LHX",
    "MJN": "RBGLY", "MYL": "VTRS", "XLNX": "AMD", "TSO": "MPC",
    "UTX": "RTX", "ARNC": "AA", "WYN": "WH"
}

def is_ticker_active(ticker: str) -> bool:
    try:
        info = yf.Ticker(ticker).info
        return bool(info and info.get("regularMarketPrice") and info.get("exchange"))
    except Exception:
        return False

def fetch_data_for_ticker(ticker: str, start: str, end: str) -> pd.DataFrame | None:
    try:
        df = yf.download(ticker, start=start, end=end, progress=False)
        if not df.empty:
            return df
        # Try fallback: last 1 year
        recent_start = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        df_recent = yf.download(ticker, start=recent_start, end=end, progress=False)
        if not df_recent.empty:
            print(f"[!] {ticker} has no data in full range but returned recent data.")
            return df_recent
        return None
    except Exception as e:
        print(f"[⚠] Exception fetching {ticker}: {e}")
        return None

def save_data(ticker: str, df: pd.DataFrame, start: str, end: str):
    filename = f"{ticker}_{start[:4]}_{end[:4]}.csv"
    filepath = os.path.join(DATA_DIR, filename)
    df.reset_index(inplace=True)
    df.to_csv(filepath, index=False)
    print(f"[✔] Saved data for {ticker} to {filepath}")

def fetch_all_valid_tickers_data(start="2018-01-01", end="2024-12-31"):
    tickers = get_unique_tickers()
    failed = []
    success = []

    for original_ticker in tickers:
        ticker = original_ticker.strip().upper()
        redirect = ticker_redirects.get(ticker, ticker)

        if redirect is None:
            print(f"[↯] {ticker} has no valid replacement. Skipping.")
            failed.append(ticker)
            continue
        elif redirect != ticker:
            print(f"[↪] Redirecting {ticker} → {redirect}")
            ticker = redirect

        if not is_ticker_active(ticker):
            print(f"[✘] {ticker} appears inactive or delisted.")
            failed.append(original_ticker)
            continue

        df = fetch_data_for_ticker(ticker, start, end)
        if df is not None:
            save_data(original_ticker, df, start, end)
            success.append(original_ticker)
        else:
            print(f"[X] No data for {original_ticker} ({ticker})")
            failed.append(original_ticker)

        time.sleep(1)

    print("\n✅ Summary:")
    print(f"Successful tickers: {len(success)}")
    print(f"Failed tickers: {len(failed)}")
    print("Failed tickers list:")
    print(failed)

    return success, failed

if __name__ == "__main__":
    fetch_all_valid_tickers_data()


