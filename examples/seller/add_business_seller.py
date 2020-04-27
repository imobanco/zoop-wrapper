import os

from pycpfcnpj import gen

from zoop_wrapper import ZoopWrapper
from zoop_wrapper import Seller, Address, Person
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

t = Seller(
    business_name="foo",
    business_phone="foo",
    business_email="foo",
    business_website="foo",
    business_opening_date="foo",
    ein=gen.cnpj(),
    owner=Person(
        first_name="foo",
        last_name="foo",
        email="foo",
        taxpayer_id=gen.cpf(),
        phone_number="foo",
        birthdate='foo',
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
    ),
    business_address=Address(
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

data = t.to_dict()

response = client.add_seller(data)

dump_response(response, os.path.basename(__file__).split(".")[0])
