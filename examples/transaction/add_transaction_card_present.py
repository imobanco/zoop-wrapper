import os

from zoop_wrapper import ZoopWrapper, Transaction, Card, Source, Token
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

seller_brian = "0b05a360f4b749498f74e13004c08024"
seller_denise = "25037b2978b14e7fa5b902d9322e8426"

t = Transaction(
    customer="foo",
    on_behalf_of="bar",
    amount="1",
    reference_id="1",
    description="foo",
    payment_type="credit",
)


response = client.add_transaction(t)

dump_response(response, os.path.basename(__file__).split(".")[0])
