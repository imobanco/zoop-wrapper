import json
from os import path

from ZoopAPIWrapper.wrapper import ZoopWrapper


client = ZoopWrapper()

response = client.list_transactions()


data_dir = path.dirname(__file__) + '/../data'
with open(f'{data_dir}/transactions.json', 'w') as file:
    json.dump(response.data, file, indent=4)
