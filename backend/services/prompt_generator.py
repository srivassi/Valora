import os
import json
import pandas as pd

from .prompts import (
    RATIO_SUMMARY_TEMPLATE,
    ANOMALY_TEMPLATE,
    HYPOTHESIS_TEMPLATE,
    COMPARE_TEMPLATE,
    PROS_CONS_TEMPLATE,
    SCORE_TEMPLATE,
    STOCK_TREND_TEMPLATE,
    TAAPI_TEMPLATE,
    HISTORICAL_FEATURES_TEMPLATE,
    OVERALL_ANALYSIS_TEMPLATE
)

def normalise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize dataframe column names to lowercase with underscores.
    Removes problematic characters for consistency in downstream processing.
    """
    df.columns = [
        col.strip().lower().replace(" ", "_").replace(".", "_").replace("-", "_")
        for col in df.columns
    ]
    return df

def generate_prompt(
    prompt_type: str,
    question: str = "",
    persona: str = "general",
    ticker: str = "",
    ratios_summary: str = "",
    anomaly_summary: str = "",
    data_summary: str = "",
    comparison_summary: str = "",
    ticker1: str = "",
    ticker2: str = "",
    year1: str = "",
    year2: str = "",
    mean1: float = 0.0,
    mean2: float = 0.0,
    t_statistic: float = 0.0,
    p_value: float = 1.0,
    taapi_summary: str = "",
    stock_summary: str = "",
    historical_summary: str = ""
) -> str:
    """
    Dynamically generate a Gemini prompt string using appropriate templates.
    Falls back to placeholder text if any key content is missing.
    """
    def format_ticker(t): return str(t).upper() if t else "UNKNOWN"
    def fallback(text, label): return text.strip() if text.strip() else f"⚠️ No {label} data available."

    prompt_type = prompt_type.strip().lower()
    persona = str(persona).strip().title()

    if prompt_type == "ratios":
        return RATIO_SUMMARY_TEMPLATE.format(
            question=question,
            persona=persona,
            ticker=format_ticker(ticker),
            ratios_summary=fallback(ratios_summary, "ratio summary")
        )

    elif prompt_type == "anomalies":
        return ANOMALY_TEMPLATE.format(
            question=question,
            ticker=format_ticker(ticker),
            anomaly_summary=fallback(anomaly_summary, "anomaly")
        )

    elif prompt_type == "hypothesis":
        return HYPOTHESIS_TEMPLATE.format(
            question=question,
            ticker=format_ticker(ticker),
            year1=year1,
            year2=year2,
            mean1=mean1,
            mean2=mean2,
            t_statistic=t_statistic,
            p_value=p_value
        )

    elif prompt_type == "compare":
        return COMPARE_TEMPLATE.format(
            question=question,
            ticker1=format_ticker(ticker1),
            ticker2=format_ticker(ticker2),
            comparison_summary=fallback(comparison_summary, "comparison summary")
        )

    elif prompt_type == "pros_cons":
        return PROS_CONS_TEMPLATE.format(
            question=question,
            persona=persona,
            ticker=format_ticker(ticker),
            data_summary=fallback(data_summary, "pros/cons data")
        )

    elif prompt_type == "score":
        return SCORE_TEMPLATE.format(
            question=question,
            persona=persona,
            ticker=format_ticker(ticker),
            data_summary=fallback(data_summary, "scoring data")
        )

    elif prompt_type == "stock_trend":
        return STOCK_TREND_TEMPLATE.format(
            question=question,
            ticker=format_ticker(ticker),
            data_summary=fallback(data_summary, "stock trend data")
        )

    elif prompt_type == "taapi":
        return TAAPI_TEMPLATE.format(
            question=question,
            ticker=format_ticker(ticker),
            data_summary=fallback(taapi_summary, "technical indicator (TAAPI)")
        )

    elif prompt_type == "historical_features":
        return HISTORICAL_FEATURES_TEMPLATE.format(
            question=question,
            ticker=format_ticker(ticker),
            data_summary=fallback(historical_summary, "historical feature")
        )

    elif prompt_type == "overall_analysis":
        return OVERALL_ANALYSIS_TEMPLATE.format(
            question=question,
            ticker=format_ticker(ticker),
            ratios_summary=fallback(ratios_summary, "ratio summary"),
            taapi_summary=fallback(taapi_summary, "TAAPI"),
            stock_summary=fallback(stock_summary, "stock data"),
            historical_summary=fallback(historical_summary, "historical feature")
        )

    return f"User asked: {question}\n\n❌ Unsupported prompt type: '{prompt_type}'"
