import os

from factory.faker import Faker

from zoop_wrapper import ZoopWrapper, Token
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


from examples.seller.retrieve_seller import seller_id  # noqa

customer_id = seller_id


response = client.add_card(card_token, customer_id)

dump_response(response, os.path.basename(__file__).split(".")[0])
