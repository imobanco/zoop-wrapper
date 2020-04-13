import os

from zoop_wrapper.wrapper import ZoopWrapper
from zoop_wrapper.models.transaction import Transaction
from zoop_wrapper.models.card import Card
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py. 
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

t = Transaction(
    customer="foo",
    on_behalf_of="bar",
    amount="1",
    reference_id="1",
    description="foo",
    payment_type="credit",
    payment_method=Card(
        expiration_year="2021", holder_name="foo", expiration_month="08"
    ),
)

data = t.to_dict()

response = client.add_transaction(data)

dump_response(response, os.path.basename(__file__).split(".")[0])
