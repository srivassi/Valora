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

def normalise_columns(df):
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
    if prompt_type == "ratios":
        return RATIO_SUMMARY_TEMPLATE.format(
            question=question,
            persona=persona,
            ticker=ticker,
            ratios_summary=ratios_summary
        )
    elif prompt_type == "anomalies":
        return ANOMALY_TEMPLATE.format(
            question=question,
            ticker=ticker,
            anomaly_summary=anomaly_summary
        )
    elif prompt_type == "hypothesis":
        return HYPOTHESIS_TEMPLATE.format(
            question=question,
            ticker=ticker,
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
            ticker1=ticker1,
            ticker2=ticker2,
            comparison_summary=comparison_summary
        )
    elif prompt_type == "pros_cons":
        return PROS_CONS_TEMPLATE.format(
            question=question,
            persona=persona,
            ticker=ticker,
            data_summary=data_summary
        )
    elif prompt_type == "score":
        return SCORE_TEMPLATE.format(
            question=question,
            persona=persona,
            ticker=ticker,
            data_summary=data_summary
        )
    elif prompt_type == "stock_trend":
        return STOCK_TREND_TEMPLATE.format(
            question=question,
            ticker=ticker,
            data_summary=data_summary
        )
    elif prompt_type == "taapi":
        return TAAPI_TEMPLATE.format(
            question=question,
            ticker=ticker,
            data_summary=taapi_summary
        )
    elif prompt_type == "historical_features":
        return HISTORICAL_FEATURES_TEMPLATE.format(
            question=question,
            ticker=ticker,
            data_summary=historical_summary
        )
    elif prompt_type == "overall_analysis":
        return OVERALL_ANALYSIS_TEMPLATE.format(
            question=question,
            ticker=ticker,
            ratios_summary=ratios_summary,
            taapi_summary=taapi_summary,
            stock_summary=stock_summary,
            historical_summary=historical_summary
        )
    else:
        return f"User asked: {question}\n\n❌ Sorry, unsupported prompt type: {prompt_type}"
