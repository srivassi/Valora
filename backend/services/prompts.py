RATIO_SUMMARY_TEMPLATE = """
You are a financial analyst tasked with reviewing the key financial ratios for {ticker} over the past 3 years.

Here is a summary of its liquidity, profitability, leverage, and efficiency metrics:

{ratios_summary}

Please:
- Identify any observable trends (e.g., improving, declining, or stable)
- Highlight key financial strengths, weaknesses, or red flags
- Summarize the overall financial health and recent performance in 2–3 sentences
- Use bullet points where appropriate
- Keep the tone clear, concise, and suitable for an investor report
"""

ANOMALY_TEMPLATE = """
You are a financial analyst reviewing companies flagged for anomalies in their financial statements.

The following entries have been marked as anomalous compared to the rest of the dataset:

{anomaly_summary}

Instructions:
- Briefly explain what might cause such anomalies (e.g., sudden drop in revenue, sharp rise in debt)
- Suggest what investors should investigate or be cautious about
- Write in a concise, professional tone
"""

HYPOTHESIS_TEMPLATE = """
A hypothesis test was conducted to evaluate changes in net margin for the company {ticker} between two periods: {year1} and {year2}.

Summary of results:
- Mean Net Margin in {year1}: {mean1:.2f}
- Mean Net Margin in {year2}: {mean2:.2f}
- t-statistic: {t_statistic:.2f}
- p-value: {p_value:.4f}

Instructions:
- Interpret whether this change appears statistically significant
- Suggest what factors could contribute to the difference in performance
- Provide your explanation in a brief and analytical format
"""

COMPARE_TEMPLATE = """
You are a financial analyst comparing two companies: {ticker1} and {ticker2}.

Below is a summary of their key financial ratios and historical returns:

{comparison_summary}

Instructions:
- Compare liquidity, profitability, market cap, and returns
- Point out which company shows stronger fundamentals
- Write in a concise, investor-facing tone
- Use bullet points and a short paragraph summary
"""
