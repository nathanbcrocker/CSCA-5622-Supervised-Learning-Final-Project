import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_bitcoin_data(days=365):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        data = response.json()
        
        prices = data['prices']
        market_caps = data['market_caps']
        total_volumes = data['total_volumes']
        
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['market_cap'] = [item[1] for item in market_caps]
        df['total_volume'] = [item[1] for item in total_volumes]
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        return df
    
    except requests.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return None

def main():
    bitcoin_data = fetch_bitcoin_data()
    
    if bitcoin_data is not None:
        print(bitcoin_data.head())
        print(f"\nShape of the dataset: {bitcoin_data.shape}")
        
        bitcoin_data.to_csv('bitcoin_data.csv')
        print("\nData saved to 'bitcoin_data.csv'")

if __name__ == "__main__":
    main()
