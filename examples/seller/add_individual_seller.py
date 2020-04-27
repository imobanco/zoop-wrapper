import os

from pycpfcnpj import gen

from zoop_wrapper import ZoopWrapper
from zoop_wrapper import Seller, Address
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

s = Seller(
    taxpayer_id=gen.cpf(),
    first_name='foo',
    last_name='foo',
    email='foo@bar.com',
    phone_number='+55 84 99999-9999',
    birthdate='1994-12-27',
    address=Address(
        line1='foo',
        line2='123',
        line3='barbar',
        neighborhood='fooofoo',
        city='Natal',
        state='RN',
        postal_code='59152250',
        country_code="BR"
    )
)


response = client.add_seller(s)

dump_response(response, os.path.basename(__file__).split(".")[0])
