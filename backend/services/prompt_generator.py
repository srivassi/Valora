# prompt_generator.py
import os
import json
import pandas as pd
from .prompts import ANOMALY_TEMPLATE, HYPOTHESIS_TEMPLATE, RATIO_SUMMARY_TEMPLATE

# 📊 Ratio Summary
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

# 🚨 Anomalies
def generate_anomaly_prompt(df_anomalies: pd.DataFrame) -> str:
    flagged = df_anomalies[df_anomalies["anomaly"] == 1]
    summary = ""

    for _, row in flagged.iterrows():
        ticker = row['Ticker.Symbol']
        period = row['Period.Ending']
        anomalous_cols = row.drop(['Ticker.Symbol', 'Period.Ending', 'anomaly'])
        metrics = [col for col in anomalous_cols.index if pd.notnull(anomalous_cols[col])]
        summary += f"- Ticker: {ticker}, Period: {period}, Anomalous Metrics: {', '.join(metrics)}\n"

    return ANOMALY_TEMPLATE.format(anomaly_summary=summary)

# 📈 Enhanced Hypothesis
def generate_enhanced_hypothesis_prompt(ticker: str) -> str:
    path = os.path.join("backend", "data", "taapi_hyptest_results", f"{ticker}_hypothesis_results.json")
    if not os.path.exists(path):
        return f"❌ No enhanced hypothesis test results found for {ticker}."

    with open(path, "r") as f:
        result = json.load(f)

    prompts = []
    for label, stats in result.items():
        if stats['p'] is None:
            continue
        prompts.append(HYPOTHESIS_TEMPLATE.format(
            ticker=ticker,
            year1="Before Signal",
            year2="After Signal",
            mean1=round(stats["signals"] - stats["successes"], 2),
            mean2=round(stats["successes"], 2),
            t_statistic=0.0,
            p_value=stats["p"]
        ))
    return "\n\n".join(prompts)

# 📉 Stock Trend Summary
def generate_stock_trend_prompt(ticker: str) -> str:
    path = os.path.join("backend", "data", "useful_database", "stock_data", f"{ticker}_historical_features.csv")
    if not os.path.exists(path):
        return f"❌ No stock trend data found for {ticker}."

    df = pd.read_csv(path).tail(30)

    try:
        rsi_trend = df["rsi"].dropna().rolling(5).mean().iloc[-1]
        macd_trend = df["macd"].dropna().rolling(5).mean().iloc[-1]
        close = df["Close"].iloc[-1]
        bb_upper = df["bb_upper"].iloc[-1]
        bb_lower = df["bb_lower"].iloc[-1]
        volatility = df["volatility_21d"].dropna().iloc[-1]

        summary = f"""
Recent stock trend summary for {ticker}:
- Current RSI (5-day avg): {rsi_trend:.2f}
- MACD (5-day avg): {macd_trend:.2f}
- Latest Close Price: {close:.2f}
- Bollinger Bands: Upper={bb_upper:.2f}, Lower={bb_lower:.2f}
- 21-day Volatility: {volatility:.4f}

Analyze this data to give a brief insight into the trend direction, volatility, and possible technical signals.
"""
        return summary.strip()
    except Exception as e:
        return f"❌ Failed to generate trend summary: {str(e)}"

def generate_comparison_prompt(ticker1: str, ticker2: str, df_ratios: pd.DataFrame) -> str:
    df_filtered = df_ratios[df_ratios["Ticker.Symbol"].isin([ticker1, ticker2])].sort_values(
        by="Period.Ending", ascending=False
    )

    summary = ""
    for ticker in [ticker1, ticker2]:
        latest = df_filtered[df_filtered["Ticker.Symbol"] == ticker].head(1)
        if latest.empty:
            continue
        row = latest.iloc[0]
        summary += f"\n{ticker}:\n"
        for col in row.index:
            if col not in ["Ticker.Symbol", "Period.Ending"]:
                summary += f"  {col}: {row[col]:.2f}\n"

    return COMPARE_TEMPLATE.format(ticker1=ticker1, ticker2=ticker2, comparison_summary=summary)
