import os

from factory.faker import Faker

from zoop_wrapper import ZoopWrapper, Transaction, Source, Token, InstallmentPlan
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

seller_brian = "0b05a360f4b749498f74e13004c08024"
seller_denise = "25037b2978b14e7fa5b902d9322e8426"

# Essa flag indica se a transação deve ser apenas pré autorizada ou capturada
capture_flag = True

# Equivalente à R$543,21
quantia_em_centavos = "54321"

t = Transaction(
    customer=seller_brian,
    description="Uma descrição breve da motivação da sua transação",
    on_behalf_of=seller_denise,
    payment_type="credit",
    capture=capture_flag,
    source=Source(
        amount=quantia_em_centavos,
        card=Token(
            card_number=Faker("credit_card_number").generate(),
            expiration_month="05",
            expiration_year="2030",
            holder_name="foo",
            security_code=123,
        ),
        usage="single_use",
        installment_plan=InstallmentPlan(
            number_installments=11,
            mode="interest_free",
        ),
    ),
)


response = client.add_transaction(t)

dump_response(response, os.path.basename(__file__).split(".")[0])
