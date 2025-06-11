import yfinance as yf
import os
import pandas as pd
from backend.utils.ticker_loader import get_unique_tickers

DATA_DIR = os.path.join("data", "stock_data")


def fetch_stock_data(ticker: str, start: str = "2020-01-01", end: str = "2024-12-31", save: bool = True) -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end)
    df.reset_index(inplace=True)
    if save:
        os.makedirs(DATA_DIR, exist_ok=True)
        filename = f"{ticker}_{start[:4]}_{end[:4]}.csv"
        path = os.path.join(DATA_DIR, filename)
        df.to_csv(path, index=False)
    return df


def fetch_all_stock_data(start: str = "2020-01-01", end: str = "2024-12-31"):
    tickers = get_unique_tickers()
    for ticker in tickers:
        print(f"Fetching stock data for {ticker}")
        fetch_stock_data(ticker, start, end, save=True)