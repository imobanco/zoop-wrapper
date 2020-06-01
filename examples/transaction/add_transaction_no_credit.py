import os

from zoop_wrapper import ZoopWrapper, Transaction, Card
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

t = Transaction(
    amount="1",
    currency="BRL",
    description="foo",
    on_behalf_of="27e17b778b404a83bf8e25ec995e2ffe",
    payment_type="credit",
    token="4abf4010cc93414ca585463fdc7b44d6",
)

response = client.add_transaction(t)

dump_response(response, os.path.basename(__file__).split(".")[0])
