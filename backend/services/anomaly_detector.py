from sklearn.ensemble import IsolationForest
import pandas as pd
from sklearn.preprocessing import StandardScaler


def detect_anomalies(df: pd.DataFrame, features: list) -> pd.DataFrame:
    df = df.copy()
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[features])
    model = IsolationForest(contamination=0.1, random_state=42)
    df["anomaly"] = model.fit_predict(df_scaled)
    df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})
    return df

