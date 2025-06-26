RATIO_SUMMARY_TEMPLATE = """
User asked: "{question}"

You are advising a {persona} investor. Evaluate {ticker}'s financial performance over the past 3 years using:

{ratios_summary}

Instructions:
- Bullet key points (under 10 words each)
- Highlight trends, red flags, contradictions
- Keep it under 100 words
- End with 2-line investor summary
- Formal, investor-facing tone
"""

ANOMALY_TEMPLATE = """
User asked: "{question}"

You are a financial analyst reviewing anomalies in {ticker}'s financials.

Detected anomalies:
{anomaly_summary}

Instructions:
- Bullet each anomaly
- Note likely cause (market vs mismanagement)
- End with 2 investor recommendations
- Use concise professional tone
"""

HYPOTHESIS_TEMPLATE = """
User asked: "{question}"

A hypothesis test was conducted on {ticker}'s net margin:

- {year1} Mean Net Margin: {mean1:.2f}
- {year2} Mean Net Margin: {mean2:.2f}
- t-stat: {t_statistic:.2f}, p-value: {p_value:.4f}

Instructions:
- Interpret significance
- 3 bullets (≤12 words)
- Max 80 words
"""

COMPARE_TEMPLATE = """
User asked: "{question}"

You are comparing {ticker1} vs {ticker2}.

Key financials:
{comparison_summary}

Instructions:
- Group by Liquidity, Profitability, Solvency, Efficiency
- 2–3 bullets per group
- Identify stronger firm
- End with short verdict
"""

PROS_CONS_TEMPLATE = """
User asked: "{question}"

You are advising a {persona} investor on {ticker}.

Metrics:
{data_summary}

Instructions:
- List 3 pros (reasons to invest)
- List 3 cons (risks)
- Use short bullet points
- End with 1-line recommendation
"""

SCORE_TEMPLATE = """
User asked: "{question}"

You are scoring {ticker} for a {persona} investor.

Financial summary:
{data_summary}

Instructions:
- Score out of 100
- 3 bullet justifications (≤12 words)
- End with 1-line investor verdict
"""

STOCK_TREND_TEMPLATE = """
User asked: "{question}"

You are analyzing short-term stock trends for {ticker}.

Recent indicators:
{data_summary}

Instructions:
- Bullet 3 key indicators (e.g., RSI, MACD, Volatility)
- Mention trend direction (bullish, bearish, neutral)
- Keep response concise and technical
- End with 1-line summary insight for short-term traders
"""

TAAPI_TEMPLATE = """
User asked: "{question}"

You are analyzing {ticker}'s technical indicators (TAAPI).

Here is the raw TAAPI data:
{data_summary}

Instructions:
- Summarize trends across MACD, RSI, EMAs
- Use up to 5 bullet points
- End with 1-line technical recommendation
"""

HISTORICAL_FEATURES_TEMPLATE = """
User asked: "{question}"

You are evaluating historical features for {ticker}.

Feature summary:
{data_summary}

Instructions:
- Note any anomalies, volatility, moving averages
- Focus on recent patterns
- Conclude with a short insight on historical stability
"""

OVERALL_ANALYSIS_TEMPLATE = """
User asked: "{question}"

Provide an overall financial analysis of {ticker} using all available data.

Financial Summary:
{ratios_summary}

TAAPI:
{taapi_summary}

Stock Data:
{stock_summary}

Historical Features:
{historical_summary}

Instructions:
- Start with financial strengths/weaknesses
- Analyze technical signals
- Highlight anomalies or inconsistencies
- End with a 2-line investor verdict
"""
