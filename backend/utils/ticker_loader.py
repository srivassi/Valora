import pandas as pd
import os

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


def get_unique_tickers(csv_filename: str = "clean_fundamentals.csv") -> list:
    current_dir = os.path.dirname(os.path.abspath(__file__))  # backend/utils
    project_root = os.path.dirname(os.path.dirname(current_dir))  # Valora/
    csv_path = os.path.join(project_root, "data", csv_filename)
    df = pd.read_csv(csv_path)

    ticker_col = "Ticker.Symbol"
    raw_tickers = df[ticker_col].dropna().unique().tolist()

    # Apply redirects
    updated_tickers = []
    for ticker in raw_tickers:
        if ticker in ticker_redirects:
            new_ticker = ticker_redirects[ticker]
            if new_ticker:  # Skip if mapped to None
                updated_tickers.append(new_ticker)
        else:
            updated_tickers.append(ticker)

    # Remove duplicates while preserving order
    seen = set()
    unique_tickers = [t for t in updated_tickers if not (t in seen or seen.add(t))]
    return unique_tickers


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



if __name__ == "__main__":
    tickers = get_unique_tickers()
    print(f"✅ Found {len(tickers)} unique tickers:")
    print(tickers)