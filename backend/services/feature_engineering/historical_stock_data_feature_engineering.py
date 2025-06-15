import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

DATA_DIR = "../../../data/useful_database/stock_data"

def compute_rsi(series, window=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    ma_up = up.rolling(window=window, min_periods=window).mean()
    ma_down = down.rolling(window=window, min_periods=window).mean()
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

def compute_ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def compute_macd(series):
    ema12 = compute_ema(series, 12)
    ema26 = compute_ema(series, 26)
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def compute_stochastic(df, k_window=14, d_window=3):
    low_min = df['Low'].rolling(window=k_window).min()
    high_max = df['High'].rolling(window=k_window).max()
    stoch_k = 100 * (df['Close'] - low_min) / (high_max - low_min)
    stoch_d = stoch_k.rolling(window=d_window).mean()
    return stoch_k, stoch_d

def compute_bollinger_bands(series, window=20, num_std=2):
    ma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper = ma + num_std * std
    lower = ma - num_std * std
    return upper, lower

def compute_obv(df):
    obv = [0]
    for i in range(1, len(df)):
        if df.loc[i, 'Close'] > df.loc[i-1, 'Close']:
            obv.append(obv[-1] + df.loc[i, 'Volume'])
        elif df.loc[i, 'Close'] < df.loc[i-1, 'Close']:
            obv.append(obv[-1] - df.loc[i, 'Volume'])
        else:
            obv.append(obv[-1])
    return pd.Series(obv, index=df.index)

def add_technical_features(df):
    df = df.copy()
    df['return_1d'] = df['Close'].pct_change()
    df['volatility_21d'] = df['return_1d'].rolling(21).std()
    df['ma_20'] = df['Close'].rolling(20).mean()
    df['ma_50'] = df['Close'].rolling(50).mean()
    df['ma_200'] = df['Close'].rolling(200).mean()
    df['rsi'] = compute_rsi(df['Close'])
    df['macd'], df['macd_signal'] = compute_macd(df['Close'])
    df['ema_50'] = compute_ema(df['Close'], 50)
    df['ema_200'] = compute_ema(df['Close'], 200)
    df['stoch_k'], df['stoch_d'] = compute_stochastic(df)
    df['bb_upper'], df['bb_lower'] = compute_bollinger_bands(df['Close'])
    df['obv'] = compute_obv(df)
    return df

def detect_anomalies(df, features):
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[features].fillna(0))
    model = IsolationForest(contamination=0.1, random_state=42)
    df['anomaly'] = model.fit_predict(df_scaled)
    df['anomaly'] = df['anomaly'].map({1: 0, -1: 1})
    return df

def engineer_features_for_stock(df):
    df = add_technical_features(df)
    features = ['return_1d', 'volatility_21d', 'rsi', 'macd', 'stoch_k']
    df = detect_anomalies(df, features)
    return df

def process_all_tickers():
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    tickers = set('_'.join(f.split('_')[:-2]) for f in files)
    for ticker in tickers:
        # Find the main file (prefer the one with the longest date range)
        ticker_files = [f for f in files if f.startswith(ticker + '_')]
        if not ticker_files:
            continue
        # Pick the file with the most rows
        best_file = max(ticker_files, key=lambda f: pd.read_csv(os.path.join(DATA_DIR, f)).shape[0])
        path = os.path.join(DATA_DIR, best_file)
        try:
            df = pd.read_csv(path)
            # Clean up possible extra header row (from your sample)
            if df.columns[0] == '' or df.iloc[0, 0] == ticker:
                df = df.iloc[1:]
            # Convert columns to correct types
            for col in ['Close', 'High', 'Low', 'Open', 'Volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df = engineer_features_for_stock(df)
            out_path = os.path.join(DATA_DIR, f"{ticker}_historical_features.csv")
            df.to_csv(out_path, index=False)
            print(f"[✔] Features engineered for {ticker} → {out_path}")
        except Exception as e:
            print(f"[!] Failed for {ticker}: {e}")

if __name__ == "__main__":
    process_all_tickers()
