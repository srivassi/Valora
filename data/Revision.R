library(tidyverse)
library(dplyr)
library(lubridate)
fundamentals <- read_csv("fundamentals.csv")
glimpse(fundamentals)

fundamentals <- read_csv("fundamentals.csv")

# Add financial ratios
fundamentals_clean <- fundamentals_clean %>%
  mutate(
    current_ratio = Total.Current.Assets / Total.Current.Liabilities,
    quick_ratio = (Total.Current.Assets - Inventory) / Total.Current.Liabilities,
    cash_ratio = Cash.and.Cash.Equivalents / Total.Current.Liabilities,
    debt_equity = Total.Liabilities / Total.Equity,
    debt_ratio = Total.Liabilities / Total.Assets,
    net_margin = Net.Income / Total.Revenue,
    gross_margin = Gross.Profit / Total.Revenue,
    operating_margin = Operating.Income / Total.Revenue,
    roa = Net.Income / Total.Assets,
    roe = Net.Income / Total.Equity,
    interest_coverage = Operating.Income / Interest.Expense,
    asset_turnover = Total.Revenue / Total.Assets,
    inventory_turnover = Cost.of.Revenue / Inventory,
  )

# Drop rows with NA in key ratios
fundamentals_clean <- fundamentals_clean %>%
  drop_na(current_ratio, quick_ratio, net_margin, roe, debt_equity)

# Filter out extreme outliers
fundamentals_clean <- fundamentals_clean %>%
  filter(roe < 5, roe > -5, debt_equity < 10, debt_equity > 0)

# Label: 'Investable' if ROE > 10% and Debt/Equity < 2
fundamentals_clean <- fundamentals_clean %>%
  mutate(investable = ifelse(roe > 0.1 & debt_equity < 2, 1, 0))

write_csv(fundamentals_clean, "clean_fundamentals.csv")
