import pandas as pd
import numpy as np

# -----------------------------
# CONFIG
# -----------------------------
INPUT_PATH = "data/demand_data.csv"
OUTPUT_PATH = "data/demand_forecast.csv"

WINDOW = 7  # moving average window
Z_P10 = 1.28
Z_P90 = 1.28

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(INPUT_PATH)
df = df.sort_values(["city", "day"])

# -----------------------------
# FORECAST FUNCTION
# -----------------------------
def forecast_city(city_df):
    city_df = city_df.copy()

    # Moving average forecast (shifted to avoid leakage)
    city_df["forecast"] = (
        city_df["demand"]
        .rolling(WINDOW)
        .mean()
        .shift(1)
    )

    # Backfill early days
    city_df["forecast"] = city_df["forecast"].fillna(city_df["demand"].mean())

    # Residuals
    residuals = city_df["demand"] - city_df["forecast"]
    sigma = residuals.std()

    # Uncertainty bands
    city_df["demand_p50"] = city_df["forecast"]
    city_df["demand_p10"] = np.maximum(city_df["forecast"] - Z_P10 * sigma, 0)
    city_df["demand_p90"] = city_df["forecast"] + Z_P90 * sigma

    return city_df

# -----------------------------
# APPLY PER CITY (future-proof)
# -----------------------------
forecasted_list = []
for city, group in df.groupby("city"):
    group_forecast = forecast_city(group.drop(columns="city"))  # drop grouping col
    group_forecast["city"] = city  # add it back
    forecasted_list.append(group_forecast)

forecasted = pd.concat(forecasted_list, ignore_index=True)

# -----------------------------
# SAVE OUTPUT
# -----------------------------
forecasted[[
    "city",
    "day",
    "demand_p10",
    "demand_p50",
    "demand_p90"
]].to_csv(OUTPUT_PATH, index=False)

print("✅ Demand forecasting completed (warning-free).")
print(f"📄 Saved to {OUTPUT_PATH}")
