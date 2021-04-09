import os
from requests import HTTPError

from zoop_wrapper import ZoopWrapper, Seller, Address
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

s = Seller(
    business_address=None,
    business_email="foo",
    business_name="foo",
    business_opening_date="foo",
    business_phone="foo",
    business_website="foo",
    ein="64070465954529",
)

seller_id = "d7b33dec57cf4a51862d5e795a51acc3"

# TODO: remover esse try/except após exclarecimentos com zoop
try:
    response = client.update_seller(seller_id, s)
except HTTPError as e:
    print(e)

dump_response(response, os.path.basename(__file__).split(".")[0])


