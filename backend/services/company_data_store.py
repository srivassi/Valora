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

# 📂 Load anomalies
def load_anomalies():
    path = os.path.join(USEFUL_DB, "anomalies.csv")
    print("📂 Loading anomalies:", path)
    df = pd.read_csv(path)
    print("✅ Anomalies loaded:", df.shape)
    return df

# 📂 Load company name mappings
def load_company_names():
    path = os.path.join(USEFUL_DB, "company_name_mapping.json")
    print("📂 Loading company names:", path)
    with open(path) as f:
        return json.load(f)

# 📂 Load TAAPI hypothesis test results
def load_taapi_results(ticker):
    path = os.path.join(USEFUL_DB, "taapi_hyptest_results", f"{ticker}_hypothesis_results.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

# 📂 Load basic stock data
def load_stock_data(ticker):
    folder = os.path.join(USEFUL_DB, "stock_data")
    exact_path = os.path.join(folder, f"{ticker}.csv")
    if os.path.exists(exact_path):
        return pd.read_csv(exact_path)
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

# 🔧 Build combined company data from all sources (batch)
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
        missing = []
        company_data = merged[merged["Ticker.Symbol"] == ticker].to_dict(orient="records")

        taapi = load_taapi_results(ticker)
        if not taapi:
            missing.append("TAAPI data")

        stock_df = load_stock_data(ticker)
        stock_data = (
            stock_df.replace({np.nan: None}).to_dict(orient="records")
            if not stock_df.empty else None
        )
        if stock_data is None:
            missing.append("stock price data")

        hist_df = load_historical_features(ticker)
        hist_features = (
            hist_df.replace({np.nan: None}).to_dict(orient="records")
            if not hist_df.empty else None
        )
        if hist_features is None:
            missing.append("historical feature data")

        companies[ticker] = {
            "financials": company_data,
            "taapi": taapi,
            "stock_data": stock_data if stock_data else [],
            "historical_features": hist_features if hist_features else [],
            "missing": missing
        }

    print("✅ Loaded companies:", list(companies.keys()))
    return companies

# 🔎 NEW: Safely load individual company data and return what's missing
def safe_load_company_info(ticker):
    company = {"ticker": ticker}
    missing = []

    # Financials
    try:
        ratios_df = load_ratios()
        company_fin = ratios_df[ratios_df["Ticker.Symbol"] == ticker]
        company["financials"] = company_fin.to_dict(orient="records") if not company_fin.empty else []
        if company_fin.empty:
            missing.append("financials")
    except:
        company["financials"] = []
        missing.append("financials")

    # Anomalies
    try:
        anom_df = load_anomalies()
        flagged = anom_df[(anom_df["Ticker.Symbol"] == ticker) & (anom_df["anomaly"] == 1)]
        company["anomalies"] = flagged.to_dict(orient="records") if not flagged.empty else []
    except:
        company["anomalies"] = []

    # TAAPI hypothesis results
    taapi = load_taapi_results(ticker)
    if taapi:
        company["taapi_hypothesis"] = taapi
    else:
        company["taapi_hypothesis"] = None
        missing.append("taapi hypothesis")

    # Stock Data
    stock_df = load_stock_data(ticker)
    if not stock_df.empty:
        company["stock_data"] = stock_df.to_dict(orient="records")
    else:
        company["stock_data"] = []
        missing.append("stock data")

    # Historical Features
    hist_df = load_historical_features(ticker)
    if not hist_df.empty:
        company["historical_features"] = hist_df.to_dict(orient="records")
    else:
        company["historical_features"] = []
        missing.append("historical features")

    company["missing"] = missing
    return company

# ✅ Dev test
if __name__ == "__main__":
    company_names = load_company_names()
    print([item['symbol'] for item in company_names])
