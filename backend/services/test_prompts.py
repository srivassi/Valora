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
LOG_DIR = "logs"
TICKERS_TO_TEST = ["AAPL", "MSFT", "META"]

# === Create logs directory ===
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
    response = get_chat_response(prompt)
    print("\n🤖 Gemini Response:")
    print(response)
    save_response("ratios", ticker, prompt, response)

# === ANOMALY PROMPT TEST ===
print("\n🚨 === TESTING ANOMALY PROMPT ===")
anomaly_prompt = generate_anomaly_prompt(anomalies_df)
print("📝 Prompt:")
print(anomaly_prompt)
response = get_chat_response(anomaly_prompt)
print("\n🤖 Gemini Response:")
print(response)
save_response("anomalies", "all", anomaly_prompt, response)

# === HYPOTHESIS PROMPT TEST ===
print("\n🧪 === TESTING ENHANCED HYPOTHESIS PROMPT (AAPL) ===")
hypo_prompt = generate_enhanced_hypothesis_prompt("AAPL")
print("📝 Prompt:")
print(hypo_prompt)
response = get_chat_response(hypo_prompt)
print("\n🤖 Gemini Response:")
print(response)
save_response("hypothesis", "AAPL", hypo_prompt, response)

# === COMPARISON PROMPT TEST ===
print("\n🆚 === TESTING COMPARISON PROMPT (AAPL vs MSFT) ===")
ratios_ready_df = pd.read_csv(RATIOS_READY_PATH)
compare_prompt = generate_comparison_prompt("AAPL", "MSFT", ratios_ready_df)
print("📝 Prompt:")
print(compare_prompt)
response = get_chat_response(compare_prompt)
print("\n🤖 Gemini Response:")
print(response)
save_response("compare", "AAPL_vs_MSFT", compare_prompt, response)
