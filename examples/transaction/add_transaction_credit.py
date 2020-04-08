import os

from ZoopAPIWrapper.wrapper import ZoopWrapper
from ZoopAPIWrapper.models.transaction import Transaction
from ZoopAPIWrapper.models.card import Card
from examples.utils import dump_response


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

dump_response(response, os.path.basename(__file__).split('.')[0])
