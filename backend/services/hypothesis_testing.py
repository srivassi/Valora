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
