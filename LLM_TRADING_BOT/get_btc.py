
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
from openai import OpenAI
from textblob import TextBlob
import matplotlib.pyplot as plt
import json


def read_api_keys(file_path):
    keys = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            name, value = line.strip().split('=')
            keys[name] = value
    return keys

api_keys = read_api_keys('apikeys.txt')


api_key = api_keys.get("API_KEY")
user_id = api_keys.get("USER_ID")
category = "FINANCE"
language = "en"

def fetch_bitcoin_price(date,previous_btc):
    try:
        timestamp = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        timestamp = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')

    
    # Prepare the URL and parameters for the API request
    url = 'https://algogene.com/rest/v1/history_price'
    params = {
        'api_key': api_key,
        'count': 1,
        'instrument': 'BTCUSD',  # Assuming the instrument code for Bitcoin is 'BTCUSD'
        'interval': 'D',  # Daily interval
        'timestamp': timestamp,
        'user': user_id
    }
    
    # Set the appropriate headers
    headers = {'Content-Type': 'application/json'}
    
    # Send the request to the API
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the response was successful
    if response.status_code == 200:
        data = response.json()
        if data and 'res' in data and data['res']:
            # Assuming the response format includes a list of results under 'res'
            price_info = data['res'][0]
            return {
                'date': date,
                'open_price': price_info.get('o'),
                'close_price': price_info.get('c'),
                'high_price': price_info.get('h'),
                'low_price': price_info.get('l'),
                'volume': price_info.get('v')
            }
        else:
            print("its gonna fail")
            return "No data available for this date."
    else:
        print("gonna fail also")
        return {"close_price": previous_btc}




days = 350
iterations_per_day = 1
interval = timedelta(days=1)
start_date = datetime(2023, 4, 26)
dates = []
data = {}
previous_btc = 0
for i in range(days * iterations_per_day):
    current_date = start_date + i * interval
    dates.append(current_date)
    print(current_date)
    if i >=1 :
        prix_btc = fetch_bitcoin_price(str(current_date),previous_btc)["close_price"]
        print(prix_btc)
        previous_btc = prix_btc
        data[str(current_date)] = prix_btc
        # print(data)
    time.sleep(6)

with open('btc_data.json', 'w') as file:
    json.dump(data, file, indent=4)

with open('btc_data.json', 'r') as file:
    loaded_data = json.load(file)

print(loaded_data)

        
        
