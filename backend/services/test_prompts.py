import sys
import os
import pandas as pd

# Add project root so we can use backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import Gemini chat function and prompt templates
from backend.services.chat_interface import get_chat_response
from backend.services.prompt_generator import (
    generate_ratio_prompt
)

# Import your ratio generator
from backend.services.data_ingestion.ratio_analysis import generate_ratios

# === Load ratios from clean_fundamentals.csv ===
ratios_df = generate_ratios(r"C:\Users\priya\OneDrive\Desktop\tcs\Valora\data\clean_fundamentals.csv")

# === Generate a prompt for a company ===
ticker = "AAPL"  # Replace with a ticker you know exists in your CSV
prompt = generate_ratio_prompt(ticker, ratios_df)

# === Print prompt and Gemini's response ===
print("\n📊 Ratio Prompt:\n", prompt)
print("\n🤖 Gemini Response:\n", get_chat_response(prompt))
