import json

from ZoopAPIWrapper.wrapper import ZoopWrapper


client = ZoopWrapper()

response = client.retrieve_transaction('9ee5d17396bb4fdfa24bdddcb9563ca3')

with open('./data/transaction.json', 'w') as file:
    json.dump(response.data, file, indent=4)
