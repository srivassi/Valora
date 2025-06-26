# Load required libraries
library(ggplot2)
library(tidyr)
library(dplyr)

# Cleaned-up dataset
data <- data.frame(
  Company = c("AAPL", "NVDA", "MSFT", "GOOGL", "AVGO", "LLY", "NVO", "ABBV", "BSX", "VRTX",
              "XOM", "CVX", "EOG", "PSX", "MPC", "LMT", "BA", "GD", "TXT", "HON",
              "WMT", "PG", "KO", "PEP", "NKE", "MA", "V", "FISV", "IVZ", "WU"),
  Industry = c(rep("Technology", 5), rep("Healthcare", 5), rep("Energy", 5),
               rep("Defense", 5), rep("Consumer Goods", 5), rep("Finance", 5)),
  `Return_1Y` = c(-6.51, 9.57, 8.38, 0.2, 49.9, -7.24, -44, 14.7, 29.6, -4.92,
                  1.89, -4.29, 4.18, -9.61, -1.93, 1.87, 13, -6.53, -10.9, 4.23,
                  40.7, 8.5, 1.1, 6.2, -11.8, 19.7, 21.2, 37.4, 4.82, -30.5),
  `Return_3Y` = c(45.3, 808.6, 101, 65.2, 412.1, 181, 48.4, 37.1, 174, 85.6,
                  17, -6.08, 3.03, 28.1, 81.3, 16, 44.5, 32.8, 30.3, 23.5,
                  141, 25.4, 17.3, 30.9, -5.3, 56.7, 57.1, 28.7, -12.7, -46.2),
  `Return_5Y` = c(135, 1489, 162.4, 147.4, 829.2, 471, 147, 107, 182, 69.6,
                  138, 55.3, 126, 60.5, 332, 23.8, 2.8, 75.1, 119, 49.7,
                  142, 51.2, 34.6, 59.1, 34.2, 112.6, 122.3, 28.8, -40.6, -60.8),
  `Vol_1Y` = c(33.1, 60.4, 25.7, 31.6, 62.7, 38.5, 43.3, 28.9, 22.6, 29.5,
               23.9, 25.4, 29.2, 36.4, 36.7, 24, 40.2, 22.6, 28.5, 24.6,
               24.1, 19.5, 17.1, 20, 43, 22, 22.9, 37.4, 27.2, 27.8),
  `Vol_3Y` = c(28.6, 56, 27, 33, 45.5, 31.7, 35.3, 23.7, 21.9, 27.2,
               26.2, 25.7, 32.7, 33.6, 34.2, 21.4, 37.5, 20.2, 27.5, 21.3,
               21.5, 17.6, 15.4, 17.7, 36.3, 20.7, 19.9, 28.7, 36.2, 27.5),
  `Vol_5Y` = c(30, 52.8, 27.1, 31.1, 40.4, 31.9, 32, 23, 24.6, 29.7,
               30.2, 28.2, 39.6, 37.8, 36.5, 22.3, 42.4, 20.8, 31.7, 22.6,
               21.1, 17.4, 17.1, 17.4, 34, 25.6, 23.2, 28.8, 33.8, 28.9)
)

# Pivot longer to tidy format
returns_long <- pivot_longer(data, cols = starts_with("Return_"),
                             names_to = "Period", values_to = "Return") %>%
  mutate(Period = gsub("Return_", "", Period))

vol_long <- pivot_longer(data, cols = starts_with("Vol_"),
                         names_to = "Period", values_to = "Volatility") %>%
  mutate(Period = gsub("Vol_", "", Period))

# Merge for plotting
long_data <- left_join(returns_long, vol_long,
                       by = c("Company", "Industry", "Period"))

# Loop by industry
industries <- unique(long_data$Industry)

for (sector in industries) {
  print(
    ggplot(long_data %>% filter(Industry == sector), aes(x = Period, group = Company)) +
      geom_line(aes(y = Return, color = "Return"), size = 1.2) +
      geom_point(aes(y = Return, color = "Return"), size = 3) +
      geom_line(aes(y = Volatility, color = "Volatility"), size = 1.2, linetype = "dashed") +
      geom_point(aes(y = Volatility, color = "Volatility"), size = 3) +
      facet_wrap(~Company, ncol = 3, scales = "free_y") +
      scale_color_manual(values = c("Return" = "#1f78b4", "Volatility" = "#e31a1c")) +
      labs(title = paste("Returns & Volatility:", sector, "Industry"),
           subtitle = "Solid line = Return, Dashed line = Volatility",
           x = "Period", y = "Percentage",
           color = "Metric") +
      theme_minimal(base_size = 14) +
      theme(
        axis.text.x = element_text(angle = 45, hjust = 1),
        strip.text = element_text(size = 13, face = "bold"),
        plot.title = element_text(face = "bold"),
        legend.position = "bottom"
      )
  )
  
  readline(prompt = paste("Viewing:", sector, "industry — Press [Enter] for next."))
  }