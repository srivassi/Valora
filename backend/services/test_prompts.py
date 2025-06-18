import pandas as pd
from backend.services.chatbot_interface import get_chat_response
from backend.services.prompt_generator import (
    generate_anomaly_prompt,
    generate_hypothesis_prompt,
    generate_ratio_prompt
)

df_anomalies = pd.read_csv("sample_anomalies.csv")
prompt = generate_anomaly_prompt(df_anomalies)
print("Anomaly Prompt:\n", prompt)
print("Gemini Response:\n", get_chat_response(prompt))

hypo_result = {
    'year1_mean': 0.15,
    'year2_mean': 0.10,
    't_statistic': 2.34,
    'p_value': 0.03,
    'significant': True
}
prompt = generate_hypothesis_prompt(hypo_result, ticker="AAPL", year1="2019", year2="2021")
print("\nHypothesis Prompt:\n", prompt)
print("Gemini Response:\n", get_chat_response(prompt))

df_ratios = pd.read_csv("sample_ratios.csv")
prompt = generate_ratio_prompt("AAPL", df_ratios)
print("\nRatio Prompt:\n", prompt)
print("Gemini Response:\n", get_chat_response(prompt))
