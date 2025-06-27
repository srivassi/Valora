import os
import sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.services.chat_interface import get_chat_response
from backend.services.prompt_generator import (
    generate_ratio_prompt,
    generate_anomaly_prompt,
    generate_enhanced_hypothesis_prompt,
    generate_comparison_prompt
)
from backend.services.data_ingestion.ratio_analysis import generate_ratios

RATIOS_CSV_PATH = "C:/Users/priya/OneDrive/Desktop/tcs/Valora/data/clean_fundamentals.csv"
ANOMALIES_CSV_PATH = "C:/Users/priya/OneDrive/Desktop/tcs/Valora/data/useful_database/anomalies.csv"
RATIOS_READY_PATH = "C:/Users/priya/OneDrive/Desktop/tcs/Valora/data/useful_database/ratios.csv"
LOG_DIR = "logs"
TICKERS_TO_TEST = ["AAL", "AAP", "ABBV", "ABC", "ABT", "ADI"]

os.makedirs(LOG_DIR, exist_ok=True)

def save_response(prompt_type, identifier, prompt, response):
    filename = f"{LOG_DIR}/{prompt_type}_{identifier}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Prompt Type: {prompt_type}\n")
        f.write(f"## Identifier: {identifier}\n\n")
        f.write("### Prompt:\n")
        f.write(f"```\n{prompt}\n```\n\n")
        f.write("### Gemini Response:\n")
        f.write(f"{response}\n")

def assert_contains(response, keywords, test_name):
    print(f"🔍 Validating response for: {test_name}")
    missing = []
    for word in keywords:
        if word.lower() not in response.lower():
            missing.append(word)
    if missing:
        print(f"❌ Missing keywords: {missing}")
    else:
        print("✅ All expected keywords found.")

# === LOAD DATA ===
print("📂 Loading ratio data...")
ratios_df = generate_ratios(RATIOS_CSV_PATH)
print("📂 Loading anomaly data...")
anomalies_df = pd.read_csv(ANOMALIES_CSV_PATH)
ratios_ready_df = pd.read_csv(RATIOS_READY_PATH)

# === RATIO PROMPT TEST ===
print("\n📊 === TESTING RATIO PROMPTS ===")
for ticker in TICKERS_TO_TEST:
    print(f"\n▶️ Ticker: {ticker}")
    prompt = generate_ratio_prompt(ticker, ratios_df)
    response = get_chat_response(prompt)
    print(response)
    assert_contains(response, ["liquidity", "profitability", "risk", "efficiency"], f"Ratios: {ticker}")
    save_response("ratios", ticker, prompt, response)

# === ANOMALY PROMPT TEST ===
print("\n🚨 === TESTING ANOMALY PROMPT ===")
anomaly_prompt = generate_anomaly_prompt(anomalies_df)
response = get_chat_response(anomaly_prompt)
print(response)
assert_contains(response, ["roa", "debt", "recommendation"], "Anomaly Test")
save_response("anomalies", "all", anomaly_prompt, response)

# === ENHANCED HYPOTHESIS TEST ===
print("\n🧪 === TESTING ENHANCED HYPOTHESIS PROMPT (AAPL) ===")
hypo_prompt = generate_enhanced_hypothesis_prompt("AAPL")
response = get_chat_response(hypo_prompt)
print(response)
assert_contains(response, ["signal", "p-value", "recommendation"], "Hypothesis AAPL")
save_response("hypothesis", "AAPL", hypo_prompt, response)

# === COMPARISON TEST ===
print("\n🆚 === TESTING COMPARISON PROMPT (AAPL vs MSFT) ===")
compare_prompt = generate_comparison_prompt("AAPL", "MSFT", ratios_ready_df)
response = get_chat_response(compare_prompt)
print(response)
assert_contains(response, ["liquidity", "stronger", "verdict"], "Compare AAPL vs MSFT")
save_response("compare", "AAPL_vs_MSFT", compare_prompt, response)
