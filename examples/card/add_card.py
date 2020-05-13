import os

from zoop_wrapper import ZoopWrapper, Card, Address
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY

client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

card = Card(
            holder_name="foo",
            expiration_year="foo",
            expiration_month="foo",
            # campos opcionais?
            uri="foo",
            updated_at="foo",
            is_verified="foo",
            created_at="foo",
            customer="foo",
            verification_checklist="foo",
            first4_digits="foo",
            is_active="foo",
            last4_digits="foo",
            id="foo",
            is_valid="foo",
            metadata="foo",
            card_brand="foo",
            fingerprint="foo",
            description="foo",
            address=Address(
            line1="foo",
            line2="123",
            line3="barbar",
            neighborhood="fooofoo",
            city="Natal",
            state="RN",
            postal_code="59152250",
            country_code="BR",
            ),
            resource="foo",
)


# response = client.add_seller(card)
#
# dump_response(response, os.path.basename(__file__).split(".")[0])