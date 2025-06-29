from sklearn.ensemble import IsolationForest
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np


def detect_anomalies(df: pd.DataFrame, features: list) -> pd.DataFrame:
    df = df.copy()
    mask_invalid = (df[features] == -9999).any(axis=1)
    df["anomaly"] = 0
    df.loc[mask_invalid, "anomaly"] = 1

    # Proceed with anomaly detection only on valid rows
    valid_df = df.loc[~mask_invalid].copy()
    valid_df.replace(-9999, np.nan, inplace=True)
    valid_df.dropna(subset=features, inplace=True)
    if not valid_df.empty:
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(valid_df[features])
        model = IsolationForest(contamination=0.1, random_state=42)
        valid_df["anomaly"] = model.fit_predict(df_scaled)
        valid_df["anomaly"] = valid_df["anomaly"].map({1: 0, -1: 1})
        df.loc[valid_df.index, "anomaly"] = valid_df["anomaly"]
    return df

if __name__ == "__main__":
    df_ratios = pd.read_csv("../../../data/useful_database/ratios.csv")
    features = df_ratios.columns.difference(["Ticker.Symbol", "Period.Ending"])
    df_with_anomalies = detect_anomalies(df_ratios, features.tolist())
    df_with_anomalies.to_csv("../data_ingestion/data/anomalies.csv", index=False)
    print("✅ Anomalies saved to data/anomalies.csv")
