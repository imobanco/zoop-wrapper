import os

from zoop_wrapper import ZoopWrapper, Transaction, Source, Token
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

card_id_brian = "6408de3a490b4679adfc462810b68a85"
seller_brian = "0b05a360f4b749498f74e13004c08024"
seller_denise = "25037b2978b14e7fa5b902d9322e8426"

t = Transaction(
    source=Source(
        card=Token(id=card_id_brian, allow_empty=True), usage="single_use", amount="500"
    ),
    on_behalf_of=seller_denise,
    customer=seller_brian,
    description="Uma descrição breve da motivação da sua transação",
    statement_descriptor="Loja do Joao",
    payment_type="credit",
    allow_empty=True,
)

response = client.add_transaction(t)

dump_response(response, os.path.basename(__file__).split(".")[0])
