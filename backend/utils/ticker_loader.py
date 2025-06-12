import pandas as pd
import os

def get_unique_tickers(csv_filename: str = "clean_fundamentals.csv") -> list:
    current_dir = os.path.dirname(os.path.abspath(__file__))  # backend/utils
    project_root = os.path.dirname(os.path.dirname(current_dir))  # Valora/
    csv_path = os.path.join(project_root, "data", csv_filename)
    df = pd.read_csv(csv_path)
    ticker_col = "Ticker.Symbol"
    ticker_list = df[ticker_col].dropna().unique().tolist()
    return ticker_list

def map_invalid_tickers(ticker_list) -> list:
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



# if __name__ == "__main__":
#     tickers = get_unique_tickers()
#     print(f"✅ Found {len(tickers)} unique tickers:")
#     print(tickers)