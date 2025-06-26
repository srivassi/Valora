import os
import json
import pandas as pd

from .prompts import (
    RATIO_SUMMARY_TEMPLATE,
    ANOMALY_TEMPLATE,
    HYPOTHESIS_TEMPLATE,
    COMPARE_TEMPLATE,
    PROS_CONS_TEMPLATE,
    SCORE_TEMPLATE
)

def normalize_columns(df):
    df.columns = [
        col.strip().lower().replace(" ", "_").replace(".", "_").replace("-", "_")
        for col in df.columns
    ]
    return df


def generate_ratio_prompt(ticker: str, df_ratios: pd.DataFrame, persona: str = "general") -> str:
    df_ratios = normalize_columns(df_ratios)
    if "ticker_symbol" not in df_ratios.columns:
        return f"❌ No ratio data available for {ticker} (missing 'ticker_symbol')."

    df_ratios["ticker_symbol"] = df_ratios["ticker_symbol"].str.upper()
    df_filtered = df_ratios[df_ratios["ticker_symbol"] == ticker.upper()].sort_values("period_ending", ascending=False).head(3)

    if df_filtered.empty:
        return f"❌ No ratio data found for {ticker}. Please verify the symbol."

    summary = ""
    for _, row in df_filtered.iterrows():
        summary += f"\nYear: {row['period_ending']}\n"
        for metric, value in row.drop(['ticker_symbol', 'period_ending']).items():
            try:
                summary += f"  {metric}: {float(value):.2f}\n"
            except:
                continue

    return RATIO_SUMMARY_TEMPLATE.format(ticker=ticker.upper(), ratios_summary=summary.strip(), persona=persona)


def generate_anomaly_prompt(df_anomalies: pd.DataFrame) -> str:
    df_anomalies = normalize_columns(df_anomalies)
    if df_anomalies.empty:
        return "✅ No anomalies detected."

    required = {"ticker_symbol", "period_ending", "anomaly_type", "details"}
    if not required.issubset(df_anomalies.columns):
        return "❌ Missing required columns in anomaly dataset."

    summary = ""
    for _, row in df_anomalies.head(5).iterrows():
        summary += f"- {row['ticker_symbol']} on {row['period_ending']}: {row['anomaly_type']} — {row['details']}\n"

    return ANOMALY_TEMPLATE.format(anomaly_summary=summary.strip())


def generate_enhanced_hypothesis_prompt(ticker: str, persona: str = "general") -> str:
    path = os.path.join("backend", "data", "taapi_hyptest_results", f"{ticker.upper()}_hypothesis_results.json")
    if not os.path.exists(path):
        return f"❌ No enhanced hypothesis results for {ticker}."

    with open(path) as f:
        result = json.load(f)

    prompts = []
    for label, stats in result.items():
        if stats.get("p") is None:
            continue

        prompts.append(HYPOTHESIS_TEMPLATE.format(
            ticker=ticker.upper(),
            year1="Before Signal",
            year2="After Signal",
            mean1=round(stats.get("signals", 0) - stats.get("successes", 0), 2),
            mean2=round(stats.get("successes", 0), 2),
            t_statistic=0.0,
            p_value=stats["p"]
        ))

    return "\n\n".join(prompts) if prompts else f"❌ No valid hypothesis results for {ticker}."


def generate_hypothesis_prompt(result: dict, ticker: str, year1: str, year2: str, persona: str = "general") -> str:
    return HYPOTHESIS_TEMPLATE.format(
        ticker=ticker.upper(),
        year1=year1,
        year2=year2,
        mean1=round(result.get("mean_1", 0), 2),
        mean2=round(result.get("mean_2", 0), 2),
        t_statistic=round(result.get("t_statistic", 0), 2),
        p_value=round(result.get("p_value", 0), 4)
    )


def generate_stock_trend_prompt(ticker: str) -> str:
    path = os.path.join("backend", "data", "useful_database", "stock_data", f"{ticker.upper()}_historical_features.csv")
    if not os.path.exists(path):
        return f"❌ No stock trend data found for {ticker}."

    try:
        df = pd.read_csv(path).tail(30)
        rsi = df["rsi"].dropna().rolling(5).mean().iloc[-1]
        macd = df["macd"].dropna().rolling(5).mean().iloc[-1]
        close = df["close"].iloc[-1]
        bb_upper = df["bb_upper"].iloc[-1]
        bb_lower = df["bb_lower"].iloc[-1]
        volatility = df["volatility_21d"].dropna().iloc[-1]

        return f"""
Recent stock trend summary for {ticker.upper()}:
- Current RSI (5-day avg): {rsi:.2f}
- MACD (5-day avg): {macd:.2f}
- Latest Close Price: {close:.2f}
- Bollinger Bands: Upper={bb_upper:.2f}, Lower={bb_lower:.2f}
- 21-day Volatility: {volatility:.4f}

Give brief insights into trend direction and volatility.
""".strip()

    except Exception as e:
        return f"❌ Failed to generate stock trend: {str(e)}"


def generate_comparison_prompt(ticker1: str, ticker2: str, df_ratios: pd.DataFrame, persona: str = "general") -> str:
    df_ratios = normalize_columns(df_ratios)
    df_ratios["ticker_symbol"] = df_ratios["ticker_symbol"].str.upper()
    df_filtered = df_ratios[df_ratios["ticker_symbol"].isin([ticker1.upper(), ticker2.upper()])]
    df_sorted = df_filtered.sort_values("period_ending", ascending=False)

    summary = ""
    for ticker in [ticker1, ticker2]:
        latest = df_sorted[df_sorted["ticker_symbol"] == ticker.upper()].head(1)
        if latest.empty:
            summary += f"\n{ticker.upper()}: No recent data.\n"
            continue

        summary += f"\n{ticker.upper()}:\n"
        for col in latest.columns:
            if col not in ["ticker_symbol", "period_ending"]:
                try:
                    summary += f"  {col}: {float(latest.iloc[0][col]):.2f}\n"
                except:
                    continue

    return COMPARE_TEMPLATE.format(ticker1=ticker1.upper(), ticker2=ticker2.upper(), comparison_summary=summary.strip())


def generate_pros_cons_prompt(ticker: str, df_ratios: pd.DataFrame, persona: str = "general") -> str:
    df_ratios = normalize_columns(df_ratios)
    df_ratios["ticker_symbol"] = df_ratios["ticker_symbol"].str.upper()
    df_filtered = df_ratios[df_ratios["ticker_symbol"] == ticker.upper()].sort_values("period_ending", ascending=False).head(1)

    if df_filtered.empty:
        return f"❌ No recent ratio data for {ticker}."

    row = df_filtered.iloc[0]
    summary_lines = [
        f"{col}: {float(val):.2f}"
        for col, val in row.items()
        if col not in ["ticker_symbol", "period_ending"] and pd.notnull(val)
    ]

    return PROS_CONS_TEMPLATE.format(ticker=ticker.upper(), data_summary="\n".join(summary_lines), persona=persona)


def generate_score_prompt(ticker: str, df_ratios: pd.DataFrame, persona: str = "general") -> str:
    df_ratios = normalize_columns(df_ratios)
    df_ratios["ticker_symbol"] = df_ratios["ticker_symbol"].str.upper()
    df_filtered = df_ratios[df_ratios["ticker_symbol"] == ticker.upper()].sort_values("period_ending", ascending=False).head(1)

    if df_filtered.empty:
        return f"❌ No recent ratio data for {ticker}."

    row = df_filtered.iloc[0]
    summary_lines = [
        f"{col}: {float(val):.2f}"
        for col, val in row.items()
        if col not in ["ticker_symbol", "period_ending"] and pd.notnull(val)
    ]

    return SCORE_TEMPLATE.format(ticker=ticker.upper(), data_summary="\n".join(summary_lines), persona=persona)
