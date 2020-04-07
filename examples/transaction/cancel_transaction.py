import json

from ZoopAPIWrapper.wrapper import ZoopWrapper


client = ZoopWrapper()

card_transaction_id = '0b8361b8fdd1480783800229f87310c2'
response = client.cancel_transaction(card_transaction_id)

with open('./data/cancel_transaction.json', 'w') as file:
    json.dump(response.data, file, indent=4)
