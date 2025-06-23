import os
import pandas as pd
import json
import numpy as np

USEFUL_DB = os.path.join(os.path.dirname(__file__), "../../data/useful_database")

def load_ratios():
    return pd.read_csv(os.path.join(USEFUL_DB, "ratios.csv"))

def load_company_names():
    with open(os.path.join(USEFUL_DB, "company_name_mapping.json")) as f:
        company_names = json.load(f)
    return company_names

def load_anomalies():
    return pd.read_csv(os.path.join(USEFUL_DB, "anomalies.csv"))

def load_taapi_results(ticker):
    path = os.path.join(USEFUL_DB, "taapi_hyptest_results", f"{ticker}_hypothesis_results.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def load_stock_data(ticker):
    path = os.path.join(USEFUL_DB, "stock_data", f"{ticker}.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

def load_historical_features(ticker):
    path = os.path.join(USEFUL_DB, "stock_data", f"{ticker}_historical_features.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

def build_company_data():
    ratios = load_ratios()
    anomalies = load_anomalies()
    merged = pd.merge(
        ratios, anomalies,
        on=["Ticker.Symbol", "Period.Ending"],
        how="outer",  # include all tickers from both files
        suffixes=('', '_anomaly')
    )
    companies = {}
    for ticker in merged["Ticker.Symbol"].dropna().unique():
        company_data = merged[merged["Ticker.Symbol"] == ticker].to_dict(orient="records")
        taapi = load_taapi_results(ticker)
        stock = load_stock_data(ticker)
        hist_features = load_historical_features(ticker)
        stock_records = stock.replace({np.nan: None}).to_dict(orient="records") if not stock.empty else []
        hist_records = hist_features.replace({np.nan: None}).to_dict(
            orient="records") if not hist_features.empty else []
        companies[ticker] = {
            "financials": company_data,
            "taapi": taapi,
            "stock_data": stock_records,
            "historical_features": hist_records,
        }
    return companies

if __name__ == "__main__":
    company_names = load_company_names()
    print([item['symbol'] for item in company_names])