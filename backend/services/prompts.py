RATIO_SUMMARY_TEMPLATE = """
📊 **{ticker} Ratio Snapshot**

**Investor Persona**: {persona}  
**Question**: {question}

**Latest Ratios**  
{ratios_summary}

💡 *Keep the summary tight — call out big red flags, strengths, or trends.*
"""

ANOMALY_TEMPLATE = """
🚨 **Anomalies Detected — {ticker}**

**Question**: {question}

**Key Flags:**  
{anomaly_summary}

⚠️ Highlight which metrics are most concerning.
"""

HYPOTHESIS_TEMPLATE = """
📈 **Hypothesis Test — {ticker}**

**Question**: {question}

- 📅 Periods: {year1} vs. {year2}  
- 📊 Means: {mean1:.2f} vs. {mean2:.2f}  
- 🔬 T-Statistic: {t_statistic:.2f}, P-Value: {p_value:.4f}

💡 Interpret statistical significance briefly. What should investors take away?
"""

COMPARE_TEMPLATE = """
🆚 **Compare {ticker1} vs {ticker2}**

**Question**: {question}

{comparison_summary}

✅ Call out which company is stronger and why — focus on profitability, risk, or trend.
"""

PROS_CONS_TEMPLATE = """
👍 **Pros & 👎 Cons — {ticker}**

**Persona**: {persona}  
**Question**: {question}

{data_summary}

🎯 Stick to 2–3 points each. Be sharp and data-backed.
"""

SCORE_TEMPLATE = """
🏅 **Investment Score — {ticker}**

**Persona**: {persona}  
**Question**: {question}

{data_summary}

✅ Assign a score **/100** and justify quickly. Mention 1 strength + 1 risk.
"""

STOCK_TREND_TEMPLATE = """
📈 **Stock Trend — {ticker}**

**Question**: {question}

{data_summary}

📊 Mention price movement, volume, and recent momentum.
"""

TAAPI_TEMPLATE = """
📊 **Technical Indicators — {ticker}**

**Question**: {question}

{data_summary}

🧭 What do RSI, MACD, EMA show? Keep this bullet-style.
"""

HISTORICAL_FEATURES_TEMPLATE = """
📦 **Historical Pattern Summary — {ticker}**

**Question**: {question}

{data_summary}

📌 Spot signals, trends, or volatility patterns. Be quick + sharp.
"""

OVERALL_ANALYSIS_TEMPLATE = """
🧠 **Overall Analysis — {ticker}**

**Question**: {question}

**🔍 Ratios**  
{ratios_summary}

**📊 TAAPI**  
{taapi_summary}

**💹 Stock Trend**  
{stock_summary}

**📦 Historical Features**  
{historical_summary}

✅ Finish with: Invest / Hold / Avoid — with 1-line reason.
"""
