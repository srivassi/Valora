import os
import json
import pandas as pd
from glob import glob
from scipy.stats import binomtest

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "taapi_hyptest")
HYPOTHESIS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "taapi_hyptest_results")
os.makedirs(HYPOTHESIS_DIR, exist_ok=True)


def test_rsi_effect(df):
    successes, total_signals = 0, 0
    for i in range(len(df) - 1):
        if df.loc[i, 'rsi'] < 30:
            total_signals += 1
            if df.loc[i + 1, 'close'] > df.loc[i, 'close']:
                successes += 1
    return build_result(successes, total_signals, "RSI")


def test_macd_cross(df):
    successes, total_signals = 0, 0
    for i in range(1, len(df) - 2):
        if df.loc[i-1, 'macd'] < df.loc[i-1, 'macd_signal'] and df.loc[i, 'macd'] > df.loc[i, 'macd_signal']:
            total_signals += 1
            if df.loc[i + 2, 'close'] > df.loc[i, 'close']:
                successes += 1
    return build_result(successes, total_signals, "MACD")


def test_ema_cross(df):
    successes, total_signals = 0, 0
    for i in range(1, len(df) - 7):
        prev_diff = df.loc[i-1, 'ema_50'] - df.loc[i-1, 'ema_200']
        curr_diff = df.loc[i, 'ema_50'] - df.loc[i, 'ema_200']
        if prev_diff < 0 and curr_diff > 0:
            total_signals += 1
            if df.loc[i + 7, 'close'] > df.loc[i, 'close']:
                successes += 1
    return build_result(successes, total_signals, "EMA Golden Cross")


def test_stoch(df):
    successes, total_signals = 0, 0
    for i in range(1, len(df) - 1):
        if df.loc[i-1, 'stoch_k'] < df.loc[i-1, 'stoch_d'] and df.loc[i, 'stoch_k'] > df.loc[i, 'stoch_d']:
            if df.loc[i, 'stoch_k'] < 20:
                total_signals += 1
                if df.loc[i + 1, 'close'] > df.loc[i, 'close']:
                    successes += 1
    return build_result(successes, total_signals, "Stochastic Crossover")


def test_bbands(df):
    successes, total_signals = 0, 0
    for i in range(len(df) - 1):
        if df.loc[i, 'close'] < df.loc[i, 'bb_lower']:
            total_signals += 1
            if df.loc[i + 1, 'close'] > df.loc[i, 'close']:
                successes += 1
    return build_result(successes, total_signals, "Bollinger Bounce")


def test_obv_divergence(df, window=5):
    successes, total_signals = 0, 0
    for i in range(len(df) - window - 3):
        obv_trend = df.loc[i:i+window, 'obv'].pct_change().sum()
        price_trend = df.loc[i:i+window, 'close'].pct_change().sum()
        if obv_trend > 0.02 and price_trend <= 0.01:
            total_signals += 1
            if df.loc[i + window + 3, 'close'] > df.loc[i + window, 'close']:
                successes += 1
    return build_result(successes, total_signals, "OBV Divergence")


def build_result(successes, total_signals, label):
    if total_signals == 0:
        return {label: {"signals": 0, "successes": 0, "p": None}}
    p_value = binomtest(successes, total_signals, p=0.5, alternative='greater')
    return {label: {
        "signals": total_signals,
        "successes": successes,
        "p": round(p_value.pvalue, 6)
    }}


def run_all_tests(df):
    results = {}
    df = df.reset_index(drop=True)
    results.update(test_rsi_effect(df))
    results.update(test_macd_cross(df))
    results.update(test_ema_cross(df))
    results.update(test_stoch(df))
    results.update(test_bbands(df))
    results.update(test_obv_divergence(df))
    return results


def process_all_successful_tickers():
    json_files = glob(os.path.join(OUTPUT_DIR, "*_taapi_history.json"))
    print(f"Found {len(json_files)} tickers with data.")

    for filepath in json_files:
        ticker = os.path.basename(filepath).replace("_taapi_history.json", "")
        try:
            with open(filepath, 'r') as f:
                records = json.load(f)
            df = pd.DataFrame(records)
            result = run_all_tests(df)
            output_path = os.path.join(HYPOTHESIS_DIR, f"{ticker}_hypothesis_results.json")
            with open(output_path, 'w') as f_out:
                json.dump(result, f_out, indent=2)
            print(f"✅ {ticker}: tests completed and saved.")
        except Exception as e:
            print(f"❌ {ticker}: Failed to process → {e}")


if __name__ == "__main__":
    process_all_successful_tickers()
