import os
import pandas as pd
import json
import numpy as np

# ✅ Resolve path to data/useful_database correctly
USEFUL_DB = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/useful_database"))
print("🔎 USEFUL_DB resolves to:", USEFUL_DB)

# 📂 Load ratios
def load_ratios():
    full_path = os.path.join(USEFUL_DB, "ratios.csv")
    print("📂 Trying to load:", full_path)
    df = pd.read_csv(full_path)
    print("✅ Ratios loaded:", df.shape)
    return df

# 📂 Load company name mappings
def load_company_names():
    path = os.path.join(USEFUL_DB, "company_name_mapping.json")
    print("📂 Loading company names:", path)
    with open(path) as f:
        return json.load(f)

# 📂 Load anomaly data
def load_anomalies():
    path = os.path.join(USEFUL_DB, "anomalies.csv")
    print("📂 Loading anomalies:", path)
    df = pd.read_csv(path)
    print("✅ Anomalies loaded:", df.shape)
    return df

# 📂 Load TAAPI hypothesis test results
def load_taapi_results(ticker):
    path = os.path.join(USEFUL_DB, "taapi_hyptest_results", f"{ticker}_hypothesis_results.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

# 📂 Load basic stock data
def load_stock_data(ticker):
    folder = os.path.join(USEFUL_DB, "stock_data")
    # Try the specific file first
    exact_path = os.path.join(folder, f"{ticker}.csv")
    if os.path.exists(exact_path):
        return pd.read_csv(exact_path)
    # Fallback: find a file that starts with ticker (e.g., AAPL_2018_2024.csv)
    for file in os.listdir(folder):
        if file.startswith(ticker + "_") and file.endswith(".csv"):
            return pd.read_csv(os.path.join(folder, file))
    return pd.DataFrame()


# 📂 Load historical stock features
def load_historical_features(ticker):
    path = os.path.join(USEFUL_DB, "stock_data", f"{ticker}_historical_features.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

# 🔧 Build combined company data from all sources
def build_company_data():
    ratios = load_ratios()
    anomalies = load_anomalies()

    # ✅ Merge ratios and anomalies
    merged = pd.merge(
        ratios,
        anomalies,
        on=["Ticker.Symbol", "Period.Ending"],
        how="outer",
        suffixes=('', '_anomaly')
    )

    print("📊 Merged dataframe shape:", merged.shape)
    if "Ticker.Symbol" not in merged.columns:
        print("❌ ERROR: 'Ticker.Symbol' column missing from merged data")
        return {}

    tickers = merged["Ticker.Symbol"].dropna().unique()
    print("🔎 Found tickers:", tickers)

    companies = {}
    for ticker in tickers:
        company_data = merged[merged["Ticker.Symbol"] == ticker].to_dict(orient="records")
        taapi = load_taapi_results(ticker)
        stock = load_stock_data(ticker)
        hist_features = load_historical_features(ticker)

        companies[ticker] = {
            "financials": company_data,
            "taapi": taapi,
            "stock_data": stock.replace({np.nan: None}).to_dict(orient="records") if not stock.empty else [],
            "historical_features": hist_features.replace({np.nan: None}).to_dict(orient="records") if not hist_features.empty else []
        }

    print("✅ Loaded companies:", list(companies.keys()))
    return companies

# ✅ Dev testing only
if __name__ == "__main__":
    company_names = load_company_names()
    print([item['symbol'] for item in company_names])
