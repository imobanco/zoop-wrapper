import os

from zoop_wrapper import (
    BillingConfiguration,
    BillingInstructions,
    Invoice,
    Transaction,
    ZoopWrapper,
)
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

seller_id = "3b94dc92dbad422ea49d44364f3b7b4b"
buyer_or_seller_id = "f85c8b84749c431ab0db044812ca7a57"


quantia_em_centavos = "1000"
vencimento = "2020-08-20"
limite = "2020-08-30"

t = Transaction(
    amount=quantia_em_centavos,
    customer=buyer_or_seller_id,
    description="meu boleto gerado para teste",
    on_behalf_of=seller_id,
    payment_type="boleto",
    payment_method=Invoice(
        expiration_date=vencimento,
        payment_limit_date=limite,
        billing_instructions=BillingInstructions(
            late_fee=BillingConfiguration(
                mode=BillingConfiguration.PERCENTAGE_MODE,
                percentage=50,
                start_date=vencimento,
            ),
            interest=BillingConfiguration(
                mode=BillingConfiguration.MONTHLY_PERCENTAGE_MODE,
                percentage=50.5555555555,
                start_date=vencimento,
            ),
            discount=BillingConfiguration(
                amount=100,
                is_discount=True,
                limit_date=vencimento,
                mode=BillingConfiguration.FIXED_MODE,
            ),
        ),
    ),
)

# _data = {
#     'amount': '1000',
#     'currency': 'BRL',
#     'description': 'meu boleto gerado para teste',
#     'on_behalf_of': seller_id,
#     'customer': buyer_or_seller_id,
#     'payment_type': 'boleto',
#     'payment_method': {
#         'expiration_date': '2020-06-20',
#         'payment_limit_date': '2020-06-30',
#         'billing_instructions': {
#             'late_fee': {
#                 'mode': BillingConfiguration.PERCENTAGE_MODE,
#                 'percentage': 30,
#                 'start_date': '2020-06-20'
#             },
#             'interest': {
#                 'mode': BillingConfiguration.MONTHLY_PERCENTAGE_MODE,
#                 'percentage': 30,
#                 'start_date': '2020-06-20'
#             },
#             'discount': [{
#                 'mode': BillingConfiguration.FIXED_MODE,
#                 'amount': 300,
#                 'limit_date': '2020-06-20'
#             }]
#         }
#     }
# }

response = client.add_transaction(t)


dump_response(response, os.path.basename(__file__).split(".")[0])
