from prophet import Prophet
import pandas as pd
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Load time series data
df = pd.read_csv("data/subscriber_timeseries.csv")

final_forecasts = []

# Loop through each unique channel name
for cname in df['channel_name'].unique():
    channel_df = df[df['channel_name'] == cname][['date', 'subscribers']].dropna()

    if len(channel_df) < 2:
        print(f"⚠️ Skipping '{cname}': Not enough data to forecast.")
        continue

    channel_df.columns = ['ds', 'y']  # Prophet needs columns named 'ds' and 'y'

    model = Prophet()
    model.fit(channel_df)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Rename for readability
    forecast = forecast.rename(columns={
        'ds': 'Date',
        'yhat': 'PredictedSubscribers',
        'yhat_lower': 'LowerBound',
        'yhat_upper': 'UpperBound'
    })[['Date', 'PredictedSubscribers', 'LowerBound', 'UpperBound']]

    forecast['Channel'] = cname
    final_forecasts.append(forecast)

# Save forecast only if data is available
if final_forecasts:
    pd.concat(final_forecasts).to_csv("data/forecasted_subs.csv", index=False)
    print("✅ Forecast saved to data/forecasted_subs.csv")
else:
    print("⚠️ No channels had enough data to generate forecasts. Please run scraper.py for more data.")

