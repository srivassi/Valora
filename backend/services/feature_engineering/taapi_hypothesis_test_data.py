import requests
import pandas as pd
import time
import json
import os
from backend.utils.ticker_loader import get_unique_tickers


TAAPI_BASE = "https://taapi.p.sulu.sh"
HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TAAPI_API_KEY')}"
}
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "taapi_hyptest")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# def safe_taapi_request(indicator, symbol, extra_params=None, retries=2, delay=3):
#     for attempt in range(retries):
#         try:
#             data = fetch_indicator(indicator, symbol, extra_params)
#             time.sleep(delay)  # throttle after a successful request
#             return data
#         except requests.exceptions.HTTPError as e:
#             print(f"[HTTPError] {symbol} | {indicator} → {e}")
#             if e.response.status_code == 401:
#                 raise  # don't retry unauthorized errors
#             time.sleep(delay)
#         except Exception as e:
#             print(f"[ERROR] Attempt {attempt+1}: {symbol} | {indicator} → {e}")
#             time.sleep(delay)
#     return None


def fetch_indicator(indicator, symbol, extra_params=None):
    url = f"{TAAPI_BASE}/{indicator}"
    params = {
        "exchange": "stocks",
        "symbol": symbol,
        "interval": "1d",
        "results": 90,
        "type": "stocks"
        }
    if extra_params:
        params.update(extra_params)
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


def fetch_all_indicators(ticker):
    print(f"  Attempting to fetch all indicators for {ticker}...")

    # Store raw dictionary responses from fetch_indicator
    raw_responses = {}
    try:
        raw_responses['rsi'] = fetch_indicator("rsi", ticker)
        time.sleep(0.5)
        raw_responses['macd'] = fetch_indicator("macd", ticker)
        time.sleep(0.5)
        raw_responses['ema50'] = fetch_indicator("ema", ticker, {"period": 50})
        time.sleep(0.5)
        raw_responses['ema200'] = fetch_indicator("ema", ticker, {"period": 200})
        time.sleep(0.5)
        raw_responses['stoch'] = fetch_indicator("stoch", ticker)
        time.sleep(0.5)
        raw_responses['bbands'] = fetch_indicator("bbands", ticker)
        time.sleep(0.5)
        raw_responses['obv'] = fetch_indicator("obv", ticker)
        time.sleep(0.5)
        raw_responses['price'] = fetch_indicator("price", ticker)
        time.sleep(0.5)

        # Now, extract the actual list of values for each indicator
        # This is where we adapt to the {'key': [values]} structure
        extracted_data_lists = {}

        # Helper function to safely extract list from dict, logging if not found/invalid
        def extract_list(indicator_name, response_dict, expected_key):
            if not isinstance(response_dict, dict):
                print(
                    f"  [WARNING] {ticker} | Indicator '{indicator_name}' response was not a dictionary. Type: {type(response_dict)}. Skipping.")
                return []

            value_list = response_dict.get(expected_key)
            if not isinstance(value_list, list):
                print(
                    f"  [WARNING] {ticker} | Indicator '{indicator_name}' did not contain a list for key '{expected_key}'. Content: {response_dict}. Skipping.")
                return []
            return value_list

        extracted_data_lists['rsi'] = extract_list('rsi', raw_responses.get('rsi'), 'value')
        extracted_data_lists['macd_macd'] = extract_list('macd', raw_responses.get('macd'), 'valueMACD')
        extracted_data_lists['macd_signal'] = extract_list('macd', raw_responses.get('macd'), 'valueMACDSignal')
        extracted_data_lists['ema50'] = extract_list('ema50', raw_responses.get('ema50'), 'value')
        extracted_data_lists['ema200'] = extract_list('ema200', raw_responses.get('ema200'), 'value')
        extracted_data_lists['stoch_k'] = extract_list('stoch', raw_responses.get('stoch'), 'valueK')
        extracted_data_lists['stoch_d'] = extract_list('stoch', raw_responses.get('stoch'), 'valueD')
        extracted_data_lists['bb_upper'] = extract_list('bbands', raw_responses.get('bbands'), 'valueUpperBand')
        extracted_data_lists['bb_middle'] = extract_list('bbands', raw_responses.get('bbands'), 'valueMiddleBand')
        extracted_data_lists['bb_lower'] = extract_list('bbands', raw_responses.get('bbands'), 'valueLowerBand')
        extracted_data_lists['obv'] = extract_list('obv', raw_responses.get('obv'), 'value')
        extracted_data_lists['price'] = extract_list('price', raw_responses.get('price'), 'value')

        # Determine the minimum number of available data points across all *extracted* lists
        min_length = 90  # Start with the expected max
        for name, data_list in extracted_data_lists.items():
            if len(data_list) < min_length:
                print(f"  [INFO] {ticker} | Extracted list for '{name}' has {len(data_list)} results (expected 90).")
                min_length = len(data_list)

        if min_length == 0:
            print(f"  [ERROR] {ticker} | No common data points across all extracted indicator lists. Skipping.")
            return None

        print(
            f"  [INFO] {ticker} | Processing {min_length} data points (minimum available across all extracted lists).")

        all_data = []
        for i in range(min_length):
            entry = {
                # Ensure we get timestamp from a reliable source like price data
                # Assuming price data's dictionary structure includes a 'timestamp' key at the list item level
                "timestamp": raw_responses.get('price', {}).get(i, {}).get("timestamp"),
                # Access raw response for timestamp if it exists per item
                "close": extracted_data_lists['price'][i],
                "rsi": extracted_data_lists['rsi'][i],
                "macd": extracted_data_lists['macd_macd'][i],
                "macd_signal": extracted_data_lists['macd_signal'][i],
                "ema_50": extracted_data_lists['ema50'][i],
                "ema_200": extracted_data_lists['ema200'][i],
                "stoch_k": extracted_data_lists['stoch_k'][i],
                "stoch_d": extracted_data_lists['stoch_d'][i],
                "bb_upper": extracted_data_lists['bb_upper'][i],
                "bb_middle": extracted_data_lists['bb_middle'][i],
                "bb_lower": extracted_data_lists['bb_lower'][i],
                "obv": extracted_data_lists['obv'][i]
            }
            all_data.append(entry)

        return pd.DataFrame(all_data)

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error for {ticker}: {e.response.status_code} - {e.response.text}")
        if e.response.status_code == 401:
            print("[CRITICAL] Unauthorized: Check your TAAPI_API_KEY environment variable.")
            raise
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error for {ticker}: {e}. Check internet connection or TAAPI server status.")
    except requests.exceptions.Timeout as e:
        print(f"❌ Timeout error for {ticker}: {e}. API took too long to respond.")
    except Exception as e:
        print(f"❌ General error for {ticker}: {e} (Type: {type(e).__name__})")
    return None


def save_failed_tickers(tickers, path):
    with open(path, "w") as f:
        for t in tickers:
            f.write(t + "\n")
    print(f"[INFO] Logged {len(tickers)} failed tickers to '{path}'")


def run_for_tickers(tickers, return_hard_failures=False, max_retries=5):
    failed_tickers = []
    hard_failures = []

    for ticker in tickers:
        print(f"\nProcessing ticker: {ticker}")
        retries = 0
        retry_delay = 5
        success = False

        while retries < max_retries and not success:
            print(f"  Attempting to fetch all indicators for {ticker}...")

            try:
                df = fetch_all_indicators(ticker)
            except requests.exceptions.HTTPError as e:
                code = e.response.status_code
                print(f"❌ HTTP error for {ticker}: {code} - {e}")
                if code in (401, 403, 404, 422):
                    print(f"🚫 Permanent failure for {ticker}. Skipping.")
                    hard_failures.append(ticker)
                    break  # hard failure, don’t retry
                elif code == 504:
                    print(f"⚠️  504 Gateway Timeout. Retrying {ticker} in {retry_delay}s...")
                else:
                    print(f"⚠️  Retriable HTTP error {code}. Retrying {ticker} in {retry_delay}s...")
                retries += 1
                time.sleep(retry_delay)
                retry_delay *= 2
                continue
            except Exception as e:
                print(f"❌ Unexpected error for {ticker}: {e}")
                retries += 1
                time.sleep(retry_delay)
                retry_delay *= 2
                continue

            # Only reach this if no exception occurred
            if df is not None and not df.empty:
                json_path = os.path.join(OUTPUT_DIR, f"{ticker}_taapi_history.json")
                try:
                    with open(json_path, 'w') as f:
                        json.dump(df.to_dict(orient='records'), f, indent=2)
                    print(f"✅ Saved {len(df)} rows to {json_path}")
                    success = True
                except Exception as e:
                    print(f"🚫 Error saving JSON for {ticker}: {e}")
                    failed_tickers.append(ticker)
                    break
            else:
                print(f"🚫 Empty or None dataframe for {ticker}")
                retries += 1
                time.sleep(retry_delay)
                retry_delay *= 2

        if not success and ticker not in hard_failures:
            failed_tickers.append(ticker)

    if return_hard_failures:
        return failed_tickers, hard_failures
    return failed_tickers




def retry_failed_tickers_until_success(max_retries=5, pause_seconds=5):
    retry_log = os.path.join(OUTPUT_DIR, "hypothesis_failed_tickers.txt")
    if not os.path.exists(retry_log):
        print("[INFO] No failed tickers log found. Skipping retry loop.")
        return

    with open(retry_log, "r") as f:
        tickers_to_retry = [line.strip() for line in f if line.strip()]

    if not tickers_to_retry:
        print("[INFO] No tickers to retry. Log file was empty.")
        return

    print(f"[RETRY LOOP] Starting retry process for {len(tickers_to_retry)} tickers.")
    retries = 0
    inactive_tickers = []

    while tickers_to_retry and retries < max_retries:
        print(f"\n🔁 Retry attempt {retries + 1}/{max_retries} for {len(tickers_to_retry)} tickers.")
        failed_tickers, hard_failures = run_for_tickers(tickers_to_retry, return_hard_failures=True)

        inactive_tickers.extend(hard_failures)
        tickers_to_retry = [t for t in failed_tickers if t not in hard_failures]
        save_failed_tickers(tickers_to_retry, retry_log)

        if not tickers_to_retry:
            print("✅ All retryable tickers succeeded.")
            break

        print(f"⚠ {len(tickers_to_retry)} retryable tickers still failing. Retrying in {pause_seconds}s...")
        retries += 1
        time.sleep(pause_seconds)

    # Final status
    if tickers_to_retry:
        final_log = os.path.join(OUTPUT_DIR, "hypothesis_failed_tickers_final.txt")
        save_failed_tickers(tickers_to_retry, final_log)
        print(f"🚫 Final retry failed for {len(tickers_to_retry)} tickers. Logged to '{final_log}'.")

    if inactive_tickers:
        inactive_log = os.path.join(OUTPUT_DIR, "hypothesis_inactive_tickers.txt")
        save_failed_tickers(sorted(set(inactive_tickers)), inactive_log)
        print(f"❌ Logged {len(inactive_tickers)} inactive/delisted tickers to '{inactive_log}'.")



def main():
    initial_tickers = get_unique_tickers()
    if not initial_tickers:
        print("[ERROR] No unique tickers found. Please ensure get_unique_tickers() is working correctly.")
        return

    print(f"Starting data fetch for {len(initial_tickers)} tickers.")
    failed_tickers = run_for_tickers(initial_tickers)

    if failed_tickers:
        retry_log = os.path.join(OUTPUT_DIR, "hypothesis_failed_tickers.txt")
        save_failed_tickers(failed_tickers, retry_log)

        print(f"\n⏳ Retrying {len(failed_tickers)} failed tickers after short pause (5s)...")
        time.sleep(5)

        second_failures = run_for_tickers(failed_tickers)
        if second_failures:
            retry_log2 = os.path.join(OUTPUT_DIR, "hypothesis_failed_tickers_retry.txt")
            save_failed_tickers(second_failures, retry_log2)
            print(f"⚠ Some tickers ({len(second_failures)}) still failed after retry. Check '{retry_log2}'.")
        else:
            print("✅ All previously failed tickers succeeded on retry.")
    else:
        print("✅ All tickers succeeded on first attempt.")


if __name__ == "__main__":
    retry_failed_tickers_until_success(max_retries=5, pause_seconds=5)
    #main()

