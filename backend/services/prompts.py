# prompts.py

RATIO_SUMMARY_TEMPLATE = """
You are advising a {persona} investor. Your task is to evaluate {ticker}'s financial performance over the past 3 years using these metrics:

{ratios_summary}

Instructions:
- Use bullet points, each under 10 words
- Highlight strong trends, red flags, and improvements
- Flag contradictory metrics clearly (e.g., high profits + negative cash)
- Keep the total response under 100 words
- End with a 2-line investor summary
- Maintain a formal, investor-facing tone
"""

ANOMALY_TEMPLATE = """
You are a financial analyst reviewing anomalies in company financials.

Detected anomalies:
{anomaly_summary}

Instructions:
- Bullet each anomaly (≤10 words)
- Note likely cause (e.g. market vs mismanagement)
- Finish with 2 investor recommendations
- Use concise, clear professional tone
"""

HYPOTHESIS_TEMPLATE = """
A test was done to check net margin change for {ticker} between {year1} and {year2}:

- Mean Net Margin {year1}: {mean1:.2f}
- Mean Net Margin {year2}: {mean2:.2f}
- t-stat: {t_statistic:.2f}, p-value: {p_value:.4f}

Instructions:
- Interpret p-value significance
- 3 short bullets (≤12 words)
- Total response ≤80 words
"""

COMPARE_TEMPLATE = """
You are a financial analyst comparing {ticker1} and {ticker2}.

Summary of key financials:
{comparison_summary}

Instructions:
- Group by Liquidity, Profitability, Solvency, Efficiency
- 2–3 bullets per group (≤10 words each)
- Identify stronger firm
- End with short 2-line investor verdict
"""

PROS_CONS_TEMPLATE = """
You are advising a {persona} investor on {ticker}.

Based on these metrics:
{data_summary}

Instructions:
- List 3 Pros (reasons to invest)
- List 3 Cons (risks or concerns)
- Use short bullet points (≤10 words)
- End with a 1-line investment recommendation
"""

SCORE_TEMPLATE = """
You are advising a {persona} investor. Based on {ticker}'s financial metrics:

{data_summary}

Instructions:
- Assign investment score (0–100)
- Give 3 short justifications (≤12 words each)
- End with 1-line investor verdict
"""
