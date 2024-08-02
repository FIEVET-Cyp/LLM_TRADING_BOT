
import os

# Désactiver les optimisations oneDNN
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
import hashlib
import hmac
import base64
import requests
from urllib.parse import urlencode
import tensorflow as tf
TF_ENABLE_ONEDNN_OPTS=0
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


def read_kraken_api_keys(file_path):
    keys = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            name, value = line.strip().split('=')
            keys[name] = value
    return keys

api_keys = read_kraken_api_keys('apikeys.txt')


kraken_api_key = api_keys.get("KRAKEN_API_KEY")
kraken_api_secret = api_keys.get("KRAKEN_API_SECRET")


def create_signature(urlpath, data, secret):
    postdata = urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    signature = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(signature.digest())

    return sigdigest.decode()



def get_btc_price():
    response = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTEUR')
    return response.json()['result']['XXBTZEUR']['c'][0]


def get_kraken_portfolio():
    urlpath = '/0/private/Balance'
    url = 'https://api.kraken.com' + urlpath
    data = {
        'nonce': str(int(1000 * time.time())),
    }

    headers = {
        'API-Key': kraken_api_key,
        'API-Sign': create_signature(urlpath, data, kraken_api_secret)
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Utilisation de la fonction
# portfolio = get_kraken_portfolio()
# print(portfolio)


def place_order(pair, volume, order_type, price=None):
    urlpath = '/0/private/AddOrder'
    url = 'https://api.kraken.com' + urlpath
    data = {
        'nonce': str(int(1000 * time.time())),
        'pair': pair,
        'type': 'buy' if order_type == 'market' else 'sell',
        'ordertype': order_type,
        'volume': volume,
    }

    headers = {
        'API-Key': kraken_api_key,
        'API-Sign': create_signature(urlpath, data, kraken_api_secret)
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()

# order_response = place_order('APEEUR', volume='4', order_type='market')
# print(order_response)

# response = requests.get('https://api.kraken.com/0/public/AssetPairs')
# pairs = response.json()

def get_price(pair):
    response = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={pair}')
    return response.json()

# while True:
#     price = get_btc_price()
#     print(f'Prix actuel de BTC/EUR: {price}')
#     time.sleep(2)  # Pause de 60 secondes

