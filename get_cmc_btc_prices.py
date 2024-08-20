import requests
import time
import csv
from datetime import datetime

def get_btc_price():
    api_key = 'MY_API_KEY'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    params = {
        'symbol': 'BTC',
        'convert': 'USD'
    }

    headers = {
        'X-CMC_PRO_API_KEY': api_key
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data['data']['BTC']['quote']['USD']['price']

def append_to_csv(timestamp, price, filename='cmc_btc_prices.csv'):
    file_exists = False
    try:
        with open(filename, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'BTC Price (USD)'])
        writer.writerow([timestamp, price])

def fetch_data(num_hours, sleep_time=1):
    end_time = time.time() + (num_hours * 3600)
    while time.time() < end_time:
        try:
            price = get_btc_price()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'Time: {timestamp}, BTC Price: ${price}')
            append_to_csv(timestamp, price)
            time.sleep(sleep_time)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(sleep_time)

fetch_data(num_hours=3, sleep_time=30)