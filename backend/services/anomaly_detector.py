from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(df_ratios, contamination=0.05):
    model = IsolationForest(n_estimators=100, contamination=contamination, random_state=42)
    features = df_ratios.drop(columns=['Ticker.Symbol', 'Period.Ending'])
    df_ratios['anomaly'] = model.fit_predict(features)
    # anomaly = -1 (outlier), 1 (inlier)
    return df_ratios
