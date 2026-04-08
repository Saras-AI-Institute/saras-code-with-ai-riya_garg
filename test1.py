from modules.processor import load_data, calculate_recovery_score
df = load_data()
df = calculate_recovery_score(df)
print(df[['date','sleep_hours','heart_rate_bpm','Recovery_score']].head(10))