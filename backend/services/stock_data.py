import yfinance as yf
import os
import pandas as pd

DATA_DIR = os.path.join("data", "stock_data")


def fetch_stock_data(ticker: str, start: str = "2020-01-01", end: str = "2024-12-31", save: bool = True) -> pd.DataFrame:
    """
    Fetch historical stock data using yfinance and optionally save it to disk.

    Args:
        ticker (str): The stock symbol (e.g., 'AAPL').
        start (str): Start date in 'YYYY-MM-DD' format.
        end (str): End date in 'YYYY-MM-DD' format.
        save (bool): If True, saves the data to a CSV in the data/stock_data directory.

    Returns:
        pd.DataFrame: DataFrame containing historical price data.
    """
    df = yf.download(ticker, start=start, end=end)
    df.reset_index(inplace=True)

    if save:
        os.makedirs(DATA_DIR, exist_ok=True)
        filename = f"{ticker}_{start[:4]}_{end[:4]}.csv"
        path = os.path.join(DATA_DIR, filename)
        df.to_csv(path, index=False)

    return df


def load_cached_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Load previously saved stock data from CSV if available.
    """
    filename = f"{ticker}_{start[:4]}_{end[:4]}.csv"
    path = os.path.join(DATA_DIR, filename)

    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=["Date"])
    else:
        return fetch_stock_data(ticker, start, end, save=True)
