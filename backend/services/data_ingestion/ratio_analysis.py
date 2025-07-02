import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def generate_ratios(input_file):
    print(f"📥 Reading data from: {input_file}")
    df = pd.read_csv(input_file)

    required_columns = [
        'Ticker.Symbol', 'Period.Ending',
        'current_ratio', 'quick_ratio', 'cash_ratio',
        'debt_equity', 'debt_ratio',
        'net_margin', 'gross_margin', 'operating_margin',
        'roa', 'roe', 'interest_coverage',
        'asset_turnover', 'inventory_turnover'
    ]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"❌ Missing columns in input CSV: {missing}")

    # Filter and clean
    df_ratios = df[required_columns].copy()
    df_ratios.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_ratios.fillna(-9999, inplace=True)

    print(f"✅ Cleaned data shape: {df_ratios.shape}")

    # Scale numeric columns, but skip -9999 values
    numeric = df_ratios.iloc[:, 2:]
    mask = numeric != -9999
    scaled = numeric.copy()
    scaler = StandardScaler()
    # Fit only on valid values
    scaled_values = scaler.fit_transform(numeric.where(mask, np.nan))
    # Put back -9999 where appropriate
    scaled[:] = np.where(mask, scaled_values, -9999)

    df_scaled = pd.DataFrame(scaled, columns=numeric.columns)

    # Reattach identifier columns
    df_scaled.insert(0, 'Period.Ending', df_ratios['Period.Ending'].values)
    df_scaled.insert(0, 'Ticker.Symbol', df_ratios['Ticker.Symbol'].values)

    return df_scaled


if __name__ == "__main__":
    input_path = "C:/Users/priya/OneDrive/Desktop/tcs/Valora/data/clean_fundamentals.csv"
    output_path = "../../../data/useful_database/ratios.csv"

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate and save ratios
    df_result = generate_ratios(input_path)
    df_result.to_csv(output_path, index=False)
    print(f"✅ Ratios saved to: {output_path}")
