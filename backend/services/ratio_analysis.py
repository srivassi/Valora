import pandas as pd
from sklearn.preprocessing import StandardScaler

file_path = "backend/data/clean_fundamentals.csv"
def generate_ratios(file_path):
    df = pd.read_csv(file_path)
    ratio_cols = [
        'Ticker.Symbol', 'Period.Ending',
        'current_ratio', 'quick_ratio', 'cash_ratio',
        'debt_equity', 'debt_ratio',
        'net_margin', 'gross_margin', 'operating_margin',
        'roa', 'roe', 'interest_coverage',
        'asset_turnover', 'inventory_turnover'
    ]

    df_ratios = df[ratio_cols].dropna()
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_ratios.iloc[:, 2:])
    df_scaled = pd.DataFrame(scaled_features, columns=ratio_cols[2:])
    df_scaled[['Ticker.Symbol', 'Period.Ending']] = df_ratios[['Ticker.Symbol', 'Period.Ending']].values
    return df_scaled

if __name__ == "__main__":
    df_scaled = generate_ratios("../../data/clean_fundamentals.csv")
    df_scaled.to_csv("data/ratios.csv", index=False)
    print("Ratios saved to data/ratios.csv")

