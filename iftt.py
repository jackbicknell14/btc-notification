import os
import requests

IFTT_KEY = os.getenv('IFTT_KEY')
print(IFTT_KEY)
ifttt_webhook_url = f'https://maker.ifttt.com/trigger/TestEvent/with/key/{IFTT_KEY}'
response = requests.post(ifttt_webhook_url)
print(response.content)
