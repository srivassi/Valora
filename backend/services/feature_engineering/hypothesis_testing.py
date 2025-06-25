import pandas as pd
from scipy.stats import ttest_ind
import json
import os

def run_ttest(df: pd.DataFrame, group_col: str, value_col: str, group1, group2):
    g1 = df[df[group_col] == group1][value_col].dropna()
    g2 = df[df[group_col] == group2][value_col].dropna()
    t_stat, p_val = ttest_ind(g1, g2)
    return {"value_col": value_col, "group_col": group_col, "group1": group1, "group2": group2, "t_stat": t_stat, "p_val": p_val}


if __name__ == "__main__":
    df = pd.read_csv("../../../data/useful_database/anomalies.csv")
    df["year"] = pd.to_datetime(df["Period.Ending"]).dt.year

    results = []

    # ROA: anomalies vs normal
    results.append(run_ttest(df, "anomaly", "roa", 1, 0))

    # Debt-to-equity: 2020 vs 2023
    de_2020 = df[df["year"] == 2020]["debt_equity"].dropna()
    de_2023 = df[df["year"] == 2023]["debt_equity"].dropna()
    t_stat, p_val = ttest_ind(de_2020, de_2023)
    results.append({
        "value_col": "debt_equity", "group_col": "year",
        "group1": 2020, "group2": 2023,
        "t_stat": t_stat, "p_val": p_val
    })

    os.makedirs("data", exist_ok=True)
    with open("../../../data/hypothesis_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Hypothesis test results saved to data/hypothesis_results.json")

