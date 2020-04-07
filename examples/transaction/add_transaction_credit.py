import json

from ZoopAPIWrapper.wrapper import ZoopWrapper
from ZoopAPIWrapper.models.transaction import Transaction
from ZoopAPIWrapper.models.card import Card


client = ZoopWrapper()

t = Transaction(
    customer='foo',
    on_behalf_of='bar',
    amount='1',
    reference_id='1',
    description='foo',

    payment_type='credit',
    payment_method=Card(
        expiration_year='2021',
        holder_name='foo',
        expiration_month='08'
    )


)

data = t.to_dict()

response = client.add_transaction(data)


with open('./data/add_transaction_credit.json', 'w') as file:
    json.dump(response.data, file, indent=4)
