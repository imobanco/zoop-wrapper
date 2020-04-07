import json
from os import path

from ZoopAPIWrapper.wrapper import ZoopWrapper
from ZoopAPIWrapper.models.transaction import Transaction
from ZoopAPIWrapper.models.invoice import (
    Invoice, BillingInstructions
)


client = ZoopWrapper()

seller_id = '27e17b778b404a83bf8e25ec995e2ffe'
buyer_or_seller_id = 'e7eec0f640c14e21b35d20d58b49b584'

t = Transaction(
    amount='300',
    description='meu boleto gerado para teste',
    on_behalf_of=seller_id,
    customer=buyer_or_seller_id,
    payment_type='boleto',
    payment_method=Invoice(
        expiration_date='2020-06-20',
        payment_limit_date='2020-06-30',
        body_instructions=['instruções para o pdf do boleto!'],
    )
)

data = t.to_dict()

response = client.add_transaction(data)


data_dir = path.dirname(__file__) + '/../data'
with open(f'{data_dir}/add_transaction_invoice.json', 'w') as file:
    json.dump(response.data, file, indent=4)
