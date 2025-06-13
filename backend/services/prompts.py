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
Below are the financial ratios for {ticker} over the last 3 years:

{ratios_summary}

Please evaluate the company's financial health and performance trends based on these ratios.
"""
