# prompts.py

RATIO_SUMMARY_TEMPLATE = """
You are acting as a senior financial analyst. Your task is to evaluate {ticker}'s financial performance over the past 3 years based on the following metrics:

{ratios_summary}

Your analysis should:
- Identify and comment on observable trends (e.g., consistent growth, sudden declines, volatility)
- Flag any strengths (e.g., high margins, strong liquidity) or concerns (e.g., rising debt, falling efficiency)
- Offer a 2–3 sentence summary of overall financial health
- Format key findings using bullet points for readability
- Maintain a clear, formal, and investor-facing tone
"""

ANOMALY_TEMPLATE = """
You are a financial analyst reviewing flagged anomalies in company financial statements.

Here are the companies and periods where anomalies were detected:

{anomaly_summary}

Please:
- Identify what may have triggered these anomalies (e.g., sharp drop in revenue, increased leverage)
- Suggest whether these anomalies may indicate poor financial management, market conditions, or accounting issues
- Recommend what investors should pay closer attention to
- Present your findings clearly and professionally
"""

HYPOTHESIS_TEMPLATE = """
A hypothesis test was performed to assess changes in net margin for {ticker} between two periods: {year1} and {year2}.

Summary of the statistical test:
- Mean Net Margin in {year1}: {mean1:.2f}
- Mean Net Margin in {year2}: {mean2:.2f}
- t-statistic: {t_statistic:.2f}
- p-value: {p_value:.4f}

Your response should:
- Explain whether the change is statistically significant based on the p-value
- Offer potential reasons for the difference (e.g., operational efficiency, market conditions)
- Include a concise conclusion in 2–3 lines
"""

COMPARE_TEMPLATE = """
You are a financial analyst comparing the fundamentals of two companies: {ticker1} and {ticker2}.

Here is a summary of their most recent financial ratios and performance metrics:

{comparison_summary}

Please:
- Compare both companies in terms of liquidity, profitability, leverage, and efficiency
- Identify which company demonstrates stronger overall fundamentals
- Write an investor-friendly summary with clear, bullet-point takeaways and a short conclusion
"""

