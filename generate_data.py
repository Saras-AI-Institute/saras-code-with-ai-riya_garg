import pandas as pd
import numpy as np
from datetime import timedelta, date

# Set the start date
start_date = date(2025, 1, 1)

# Parameters
num_days = 365
missing_values_prob = 0.05
date_list = [start_date + timedelta(days=i) for i in range(num_days)]

# Generate dates
rng = pd.date_range(start_date, periods=num_days, freq='D')

# Generate synthetic data
np.random.seed(42)  # For reproducibility

steps = np.random.normal(8500, 2000, num_days).clip(3000, 18000)
sleep_hours = np.random.normal(7.2, 1.0, num_days).clip(4.5, 9.5)
heart_rate = np.random.normal(68, 10, num_days).clip(48, 110)
calories_burned = np.random.uniform(1800, 4200, num_days)
active_minutes = np.random.uniform(20, 180, num_days)

# Create a DataFrame
data = pd.DataFrame({
    'date': rng,
    'steps': steps,
    'sleep_hours': sleep_hours,
    'heart_rate_bpm': heart_rate,
    'calories_burned': calories_burned,
    'active_minutes': active_minutes
})

# Introduce missing values
for column in data.columns[1:]:  # Skip the date column
    data.loc[data.sample(frac=missing_values_prob).index, column] = np.nan

# Save to a CSV file
data.to_csv('data/health_data.csv', index=False)
