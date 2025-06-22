ANOMALY_TEMPLATE = """
You are a financial analyst. 
A machine learning model flagged the following companies as having anomalies in their financial ratios:

{anomaly_summary}

Please explain what might be causing these anomalies and what the investor should watch out for.
"""

HYPOTHESIS_TEMPLATE = """
A hypothesis test was conducted to evaluate changes in net margin for the company {ticker} between {year1} and {year2}.

Results:
- Mean Net Margin in {year1}: {mean1:.2f}
- Mean Net Margin in {year2}: {mean2:.2f}
- t-statistic: {t_statistic:.2f}
- p-value: {p_value:.4f}

Interpret these results. Is the change statistically significant? What might explain this difference?
"""

RATIO_SUMMARY_TEMPLATE = """
You are a financial analyst tasked with reviewing Apple Inc. (AAPL)'s key financial ratios over the past 3 years.

Below is a summary of its liquidity, profitability, leverage, and efficiency ratios:

{ratios_summary}

Instructions:
- Identify trends (improving, declining, or stable) across the years
- Highlight any strengths, weaknesses, or red flags
- Provide a 1-paragraph overall assessment of Apple's financial health and performance
- Use bullet points where helpful
- Keep the tone analytical but concise, as if writing for an investor report
"""

