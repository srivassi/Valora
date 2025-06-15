import os
import pandas as pd
import json

USEFUL_DB = os.path.join(os.path.dirname(__file__), "../../data/useful_database")

def load_ratios():
    return pd.read_csv(os.path.join(USEFUL_DB, "ratios.csv"))

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
    merged = pd.merge(ratios, anomalies, on=["Ticker.Symbol", "Period.Ending"], suffixes=('', '_anomaly'))
    companies = {}
    for ticker in merged["Ticker.Symbol"].unique():
        company_data = merged[merged["Ticker.Symbol"] == ticker].to_dict(orient="records")
        taapi = load_taapi_results(ticker)
        stock = load_stock_data(ticker)
        companies[ticker] = {
            "financials": company_data,
            "taapi": taapi,
            "stock_data": stock.to_dict(orient="records") if not stock.empty else [],
            "historical_features": hist_features.to_dict(orient="records") if not hist_features.empty else []
        }
    return companies
