import os
import json
import pandas as pd

from .prompts import (
    RATIO_SUMMARY_TEMPLATE,
    ANOMALY_TEMPLATE,
    HYPOTHESIS_TEMPLATE,
    COMPARE_TEMPLATE
)

# 📊 Ratio Summary
def generate_ratio_prompt(ticker: str, df_ratios: pd.DataFrame) -> str:
    df_filtered = df_ratios[df_ratios['Ticker.Symbol'] == ticker].sort_values("Period.Ending", ascending=False).head(3)
    if df_filtered.empty:
        return f"❌ No ratio data available for {ticker}."

    summary = ""
    for _, row in df_filtered.iterrows():
        summary += f"\nYear: {row['Period.Ending']}\n"
        for metric, value in row.drop(['Ticker.Symbol', 'Period.Ending']).items():
            summary += f"  {metric}: {value:.2f}\n"

    return RATIO_SUMMARY_TEMPLATE.format(ticker=ticker, ratios_summary=summary)


# 🚨 Anomaly Summary
def generate_anomaly_prompt(df_anomalies: pd.DataFrame) -> str:
    if df_anomalies.empty:
        return "No anomalies detected."

    expected_cols = ["Ticker.Symbol", "Period.Ending", "Anomaly_Type", "Details"]
    for col in expected_cols:
        if col not in df_anomalies.columns:
            raise KeyError(f"Missing column in anomalies.csv: {col}")

    summary = ""
    for _, row in df_anomalies.head(5).iterrows():
        summary += (
            f"- {row['Ticker.Symbol']} on {row['Period.Ending']}: "
            f"{row['Anomaly_Type']} — {row['Details']}\n"
        )

    return ANOMALY_TEMPLATE.format(anomaly_summary=summary)


# 🧪 Enhanced Hypothesis Prompt
def generate_enhanced_hypothesis_prompt(ticker: str) -> str:
    path = os.path.join("backend", "data", "taapi_hyptest_results", f"{ticker}_hypothesis_results.json")
    if not os.path.exists(path):
        return f"❌ No enhanced hypothesis test results found for {ticker}."

    with open(path, "r") as f:
        result = json.load(f)

    prompts = []
    for label, stats in result.items():
        if stats.get('p') is None:
            continue

        prompts.append(HYPOTHESIS_TEMPLATE.format(
            ticker=ticker,
            year1="Before Signal",
            year2="After Signal",
            mean1=round(stats.get("signals", 0) - stats.get("successes", 0), 2),
            mean2=round(stats.get("successes", 0), 2),
            t_statistic=0.0,
            p_value=stats["p"]
        ))

    return "\n\n".join(prompts) if prompts else f"❌ No valid hypothesis results for {ticker}."


# 🧪 Basic Hypothesis Prompt
def generate_hypothesis_prompt(result: dict, ticker: str, year1: str, year2: str) -> str:
    return HYPOTHESIS_TEMPLATE.format(
        ticker=ticker,
        year1=year1,
        year2=year2,
        mean1=round(result["mean_1"], 2),
        mean2=round(result["mean_2"], 2),
        t_statistic=round(result["t_statistic"], 2),
        p_value=round(result["p_value"], 4)
    )


# 📈 Stock Trend Summary
def generate_stock_trend_prompt(ticker: str) -> str:
    path = os.path.join("backend", "data", "useful_database", "stock_data", f"{ticker}_historical_features.csv")
    if not os.path.exists(path):
        return f"❌ No stock trend data found for {ticker}."

    try:
        df = pd.read_csv(path).tail(30)

        rsi = df["rsi"].dropna().rolling(5).mean().iloc[-1]
        macd = df["macd"].dropna().rolling(5).mean().iloc[-1]
        close = df["Close"].iloc[-1]
        bb_upper = df["bb_upper"].iloc[-1]
        bb_lower = df["bb_lower"].iloc[-1]
        volatility = df["volatility_21d"].dropna().iloc[-1]

        return f"""
Recent stock trend summary for {ticker}:
- Current RSI (5-day avg): {rsi:.2f}
- MACD (5-day avg): {macd:.2f}
- Latest Close Price: {close:.2f}
- Bollinger Bands: Upper={bb_upper:.2f}, Lower={bb_lower:.2f}
- 21-day Volatility: {volatility:.4f}

Analyze this data to give a brief insight into trend direction, volatility, and possible technical signals.
""".strip()

    except Exception as e:
        return f"❌ Failed to generate trend summary: {str(e)}"


# 🆚 Company Comparison
def generate_comparison_prompt(ticker1: str, ticker2: str, df_ratios: pd.DataFrame) -> str:
    df_filtered = df_ratios[df_ratios["Ticker.Symbol"].isin([ticker1, ticker2])]
    df_sorted = df_filtered.sort_values("Period.Ending", ascending=False)

    summary = ""
    for ticker in [ticker1, ticker2]:
        latest = df_sorted[df_sorted["Ticker.Symbol"] == ticker].head(1)
        if latest.empty:
            summary += f"\n{ticker}: No recent data available.\n"
            continue

        summary += f"\n{ticker}:\n"
        for col in latest.columns:
            if col not in ["Ticker.Symbol", "Period.Ending"]:
                summary += f"  {col}: {latest.iloc[0][col]:.2f}\n"

    return COMPARE_TEMPLATE.format(
        ticker1=ticker1,
        ticker2=ticker2,
        comparison_summary=summary.strip()
    )
