import json
from os import path

from ZoopAPIWrapper.wrapper import ZoopWrapper


client = ZoopWrapper()

response = client.list_transactions_for_seller('27e17b778b404a83bf8e25ec995e2ffe')


data_dir = path.dirname(__file__) + '/../data'
with open(f'{data_dir}/transactions_seller.json', 'w') as file:
    json.dump(response.data, file, indent=4)
