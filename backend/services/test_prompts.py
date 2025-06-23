import os
import sys
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# === Import services ===
from backend.services.chat_interface import get_chat_response
from backend.services.prompt_generator import (
    generate_ratio_prompt,
    generate_anomaly_prompt,
    generate_enhanced_hypothesis_prompt,
    generate_comparison_prompt
)
from backend.services.data_ingestion.ratio_analysis import generate_ratios

# === CONFIGURATION ===
RATIOS_CSV_PATH = "C:/Users/priya/OneDrive/Desktop/tcs/Valora/data/clean_fundamentals.csv"
ANOMALIES_CSV_PATH = "C:/Users/priya/OneDrive/Desktop/tcs/Valora/data/useful_database/anomalies.csv"
RATIOS_READY_PATH = "C:/Users/priya/OneDrive/Desktop/tcs/Valora/data/useful_database/ratios.csv"
TICKERS_TO_TEST = ["AAPL", "MSFT", "META"]

# === LOAD DATA ===
print("📂 Loading ratio data...")
ratios_df = generate_ratios(RATIOS_CSV_PATH)

print("📂 Loading anomaly data...")
anomalies_df = pd.read_csv(ANOMALIES_CSV_PATH)

# === RATIO PROMPT TEST ===
print("\n📊 === TESTING RATIO PROMPTS ===")
for ticker in TICKERS_TO_TEST:
    print(f"\n▶️ Ticker: {ticker}")
    prompt = generate_ratio_prompt(ticker, ratios_df)
    print("📝 Prompt:")
    print(prompt)
    print("\n🤖 Gemini Response:")
    print(get_chat_response(prompt))

# === ANOMALY PROMPT TEST ===
print("\n🚨 === TESTING ANOMALY PROMPT ===")
anomaly_prompt = generate_anomaly_prompt(anomalies_df)
print("📝 Prompt:")
print(anomaly_prompt)
print("\n🤖 Gemini Response:")
print(get_chat_response(anomaly_prompt))

# === HYPOTHESIS PROMPT TEST ===
print("\n🧪 === TESTING HYPOTHESIS PROMPT (AAPL) ===")
hypo_prompt = generate_enhanced_hypothesis_prompt("AAPL")
print("📝 Prompt:")
print(hypo_prompt)
print("\n🤖 Gemini Response:")
print(get_chat_response(hypo_prompt))

# === COMPARISON PROMPT TEST ===
print("\n🆚 === TESTING COMPARISON PROMPT (AAPL vs MSFT) ===")
ratios_ready_df = pd.read_csv(RATIOS_READY_PATH)
compare_prompt = generate_comparison_prompt("AAPL", "MSFT", ratios_ready_df)
print("📝 Prompt:")
print(compare_prompt)
print("\n🤖 Gemini Response:")
print(get_chat_response(compare_prompt))
