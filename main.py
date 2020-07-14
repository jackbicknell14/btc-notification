import requests
import json
import os

import time
from datetime import datetime

BITCOIN_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC&convert=GBP'
COINMARKETCAP_PRO_API_KEY = os.getenv('CMP')
IFTT_KEY = os.getenv('IFTT_KEY')
IFTTT_WEBHOOKS_URL = f'https://maker.ifttt.com/trigger/BTC_price_notification/with/key/{IFTT_KEY}'
BITCOIN_PRICE_THRESHOLD = 7_300


def get_latest_bitcoin_price():
    headers = {
        'Accepts': 'application/json',
        'Accept-Encoding': 'deflate, gzip',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_PRO_API_KEY,
    }
    response = requests.get(BITCOIN_API_URL, headers=headers)
    data = response.json()
    btc_latest = data['data']['BTC']['quote']['GBP']['price']
    return float(btc_latest)


def post_ifttt_webhook(value):
    data = {'value1': value}
    response = requests.post(IFTTT_WEBHOOKS_URL, json=data)
    print(response.content)


# def main():
#     price = get_latest_bitcoin_price()
#     print(price)
#     post_ifttt_webhook(value=price)


def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook(price)

        # # Send a Telegram notification
        # # Once we have 5 items in our bitcoin_history send an update
        # if len(bitcoin_history) == 5:
        #     post_ifttt_webhook('bitcoin_price_update',
        #                        format_bitcoin_history(bitcoin_history))
        #     # Reset the history
        #     bitcoin_history = []
        #
        # # Sleep for 5 minutes
        # # (For testing purposes you can set it to a lower number)
        time.sleep(5 * 60)


if __name__ == '__main__':
    main()
