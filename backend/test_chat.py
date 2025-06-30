import requests
import random
import json

ENDPOINT = "http://127.0.0.1:8000/chat"

companies = ["AAPL", "TSLA", "NVDA", "META", "AMZN", "NFLX", "JPM", "PEP", "MSFT"]

test_cases = [
    {"prompt_type": "ratios", "question": "How has their profitability changed recently?"},
    {"prompt_type": "anomalies", "question": "What financial anomalies have been found?"},
    {"prompt_type": "enhanced_hypothesis", "question": "Do RSI signals predict performance?"},
    {"prompt_type": "taapi", "question": "What are the current technical indicators saying?"},
    {"prompt_type": "stock_data", "question": "Give me the recent stock data."},
    {"prompt_type": "stock_trend", "question": "What is the trend in the stock movement?"},
    {"prompt_type": "historical_features", "question": "Show historical features."},
    {"prompt_type": "pros_cons", "question": "Summarize the investment pros and cons."},
    {"prompt_type": "score", "question": "Rate the company as an investment."},
    {"prompt_type": "overall_analysis", "question": "What does a full company analysis look like?"},
    {"prompt_type": "compare", "ticker": "AAPL vs MSFT", "question": "Which company is stronger?"}
]

print("🚀 Running test cases for /chat endpoint...\n")

for company in companies:
    for case in test_cases:
        if case["prompt_type"] == "compare":
            # Only run comparison once
            payload = {
                "prompt_type": "compare",
                "ticker": case["ticker"],
                "question": case["question"],
                "persona": "general"
            }
            print(f"🆚 Compare: {case['ticker']}")
        else:
            payload = {
                "prompt_type": case["prompt_type"],
                "ticker": company,
                "question": case["question"],
                "persona": "general"
            }
            print(f"🔹 {case['prompt_type'].capitalize()} — {company}")

        try:
            response = requests.post(ENDPOINT, json=payload)
            print(f"✅ Status: {response.status_code}")
            reply = response.json().get("reply", "[No reply received]")
            print("🧠 Reply:\n", reply[:1500])  # Truncate long replies
        except Exception as e:
            print(f"❌ Request failed: {e}")

        print("-" * 80)
