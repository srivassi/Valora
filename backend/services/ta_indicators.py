import os
import pandas as pd
import pandas_ta as ta
from backend.utils.ticker_loader import get_unique_tickers

DATA_DIR = os.path.join("data", "stock_data")
INDICATOR_DIR = os.path.join("data", "stock_indicators")


def compute_indicators_for_ticker(ticker: str, start="2020-01-01", end="2024-12-31", save=True):
    file_path = os.path.join(DATA_DIR, f"{ticker}_{start[:4]}_{end[:4]}.csv")
    if not os.path.exists(file_path):
        print(f"Stock data for {ticker} not found. Skipping.")
        return None

    df = pd.read_csv(file_path)
    if "Date" in df.columns:
        df.set_index(pd.to_datetime(df["Date"]), inplace=True)

    # Compute indicators
    df.ta.ema(length=20, append=True)
    df.ta.macd(append=True)
    df.ta.rsi(append=True)
    df.ta.stoch(append=True)
    df.ta.bbands(append=True)
    df.ta.obv(append=True)

    if save:
        os.makedirs(INDICATOR_DIR, exist_ok=True)
        indicator_path = os.path.join(INDICATOR_DIR, f"{ticker}_indicators.csv")
        df.to_csv(indicator_path)

    return df


def compute_all_indicators(start="2020-01-01", end="2024-12-31"):
    tickers = get_unique_tickers()
    for ticker in tickers:
        print(f"Computing indicators for {ticker}")
        compute_indicators_for_ticker(ticker, start, end, save=True)
