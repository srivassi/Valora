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

if __name__ == "__main__":
    df_ratios = pd.read_csv("../../data/ratios.csv")
    features = df_ratios.columns.difference(["Ticker.Symbol", "Period.Ending"])
    df_with_anomalies = detect_anomalies(df_ratios, features.tolist())
    df_with_anomalies.to_csv("../../data/anomalies.csv", index=False)
    print("✅ Anomalies saved to data/anomalies.csv")
