import cryptocompare
import pandas as pd

coins = ['BTC', 'ETH', 'ADA']
end_date = pd.Timestamp('2025-05-02')
#limit = 2000  # max days
limit = 30
all_data = {}

for coin in coins:
    print(f"Fetching {coin}...")
    data = cryptocompare.get_historical_price_day(coin, currency='USD', limit=limit, toTs=end_date.timestamp())
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    all_data[coin] = df

    df.to_csv(f'{coin}_history.csv', index=False)

# Access like: all_data['BTC']

combined_df = pd.DataFrame()

for coin in coins:
    df = all_data[coin][['time', 'close']].rename(columns={'close': f'{coin}_close'})
    if combined_df.empty:
        combined_df = df
    else:
        combined_df = pd.merge(combined_df, df, on='time', how='outer')

# Sort by time
combined_df = combined_df.sort_values('time')

# ✅ Save combined data
combined_df.to_csv('crypto_combined_history.csv', index=False)
