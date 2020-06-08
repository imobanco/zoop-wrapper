import os

from factory.faker import Faker

from zoop_wrapper import ZoopWrapper, Transaction, Token, Card
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

card_token = Token(
    holder_name="foo",
    expiration_year="2030",
    expiration_month="05",
    card_number=Faker("credit_card_number").generate(),
    security_code=123,
)

t = Transaction(
    source=card_token.to_dict(),
    on_behalf_of="27e17b778b404a83bf8e25ec995e2ffe",
    customer="0e084bb6a60f47e8ac45949d5040eb92",
    amount="1",
    description="Uma descrição breve da motivação da sua transação",
    statement_descriptor="Loja do Joao",
    payment_type="credit",
    allow_empty=True,
)

response = client.add_transaction(t)

dump_response(response, os.path.basename(__file__).split(".")[0])
