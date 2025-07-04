# 📘 Prompt Engineering Guide – Valora Chatbot

## 👤 Author
**Priyanka** – Prompt Engineer  
Role: Built, tested, and refined all Gemini prompts and integration logic

---

## 🧠 Purpose
This document explains how all prompt types work in the Valora chatbot and how they are generated dynamically using financial data.

---

## ⚙️ Prompt Types

| Prompt Type          | Description                                                  | Example Ticker |
|----------------------|--------------------------------------------------------------|----------------|
| `ratios`             | Summarizes liquidity, profitability, risk, and efficiency    | AAPL           |
| `anomalies`          | Lists companies flagged with abnormal financial patterns     | AAPL           |
| `enhanced_hypothesis`| Hypothesis testing on TAAPI indicators                       | AAPL           |
| `hypothesis`         | Compares a financial metric across two time periods          | AAPL           |
| `stock_trend`        | Summarizes recent technical trend indicators (RSI, MACD...)  | AAPL           |
| `compare`            | Compares key ratios between two companies                    | AAPL vs MSFT   |
| `overall_analysis`   | Full data dump across all sources + global insight           | AAPL           |

---

## 🛠 Prompt Generation Code

All prompts are generated using functions in:

```text
backend/services/prompt_generator.py
