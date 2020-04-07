import json

from ZoopAPIWrapper.wrapper import ZoopWrapper


client = ZoopWrapper()

response = client.list_transactions()

with open('./data/transactions.json', 'w') as file:
    json.dump(response.data, file, indent=4)
