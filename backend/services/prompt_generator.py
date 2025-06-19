# prompt_generator.py
import pandas as pd
from .prompts import ANOMALY_TEMPLATE, HYPOTHESIS_TEMPLATE, RATIO_SUMMARY_TEMPLATE

def generate_anomaly_prompt(df_anomalies: pd.DataFrame) -> str:
    flagged = df_anomalies[df_anomalies["anomaly"] == -1]
    summary = ""

    for _, row in flagged.iterrows():
        ticker = row['Ticker.Symbol']
        period = row['Period.Ending']
        anomalous_cols = row.drop(['Ticker.Symbol', 'Period.Ending', 'anomaly'])
        metrics = [col for col in anomalous_cols.index if pd.notnull(anomalous_cols[col])]
        summary += f"- Ticker: {ticker}, Period: {period}, Anomalous Metrics: {', '.join(metrics)}\n"

    return ANOMALY_TEMPLATE.format(anomaly_summary=summary)

def generate_hypothesis_prompt(result: dict, ticker: str, year1: str, year2: str) -> str:
    return HYPOTHESIS_TEMPLATE.format(
        ticker=ticker,
        year1=year1,
        year2=year2,
        mean1=result['year1_mean'],
        mean2=result['year2_mean'],
        t_statistic=result['t_statistic'],
        p_value=result['p_value']
    )

def generate_ratio_prompt(ticker: str, df_ratios: pd.DataFrame) -> str:
    summary = ""
    df_filtered = df_ratios[df_ratios['Ticker.Symbol'] == ticker].sort_values(by="Period.Ending", ascending=False).head(3)

    for _, row in df_filtered.iterrows():
        year = row['Period.Ending']
        metrics = row.drop(['Ticker.Symbol', 'Period.Ending'])
        summary += f"\nYear: {year}\n"
        for metric, value in metrics.items():
            summary += f"  {metric}: {value:.2f}\n"

    return RATIO_SUMMARY_TEMPLATE.format(ticker=ticker, ratios_summary=summary)
