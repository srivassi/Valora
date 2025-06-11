import pandas as pd
from scipy.stats import ttest_ind

def test_net_margin_difference(file_path, year1='2019', year2='2021'):
    df = pd.read_csv(file_path)
    df['Year'] = pd.to_datetime(df['Period.Ending']).dt.year

    net_margin_1 = df[df['Year'] == int(year1)]['net_margin'].dropna()
    net_margin_2 = df[df['Year'] == int(year2)]['net_margin'].dropna()

    stat, p = ttest_ind(net_margin_1, net_margin_2, equal_var=False)
    return {
        'year1_mean': net_margin_1.mean(),
        'year2_mean': net_margin_2.mean(),
        't_statistic': stat,
        'p_value': p,
        'significant': p < 0.05
    }

def run_ttest(df: pd.DataFrame, group_col: str, value_col: str, group1, group2):
    group1_data = df[df[group_col] == group1][value_col].dropna()
    group2_data = df[df[group_col] == group2][value_col].dropna()
    t_stat, p_val = ttest_ind(group1_data, group2_data)
    return {"t_stat": t_stat, "p_val": p_val}

