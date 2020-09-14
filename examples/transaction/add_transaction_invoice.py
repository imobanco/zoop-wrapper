import os

from zoop_wrapper import (
    Fine,
    Interest,
    Discount,
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
from examples.seller.retrieve_seller import seller_id
from examples.buyer.retrieve_buyer import buyer_id


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

# seller_id = "3b94dc92dbad422ea49d44364f3b7b4b"
buyer_or_seller_id = buyer_id


quantia_em_centavos = "3000"
vencimento = "2020-11-20"
pre_vencimento = "2020-11-10"
limite = "2020-11-30"

t = Transaction(
    amount=quantia_em_centavos,
    customer=buyer_or_seller_id,
    description="meu boleto gerado para teste",
    on_behalf_of=seller_id,
    capture=True,
    payment_type="boleto",
    payment_method=Invoice(
        expiration_date=vencimento,
        payment_limit_date=limite,
        billing_instructions=BillingInstructions(
            late_fee=Fine(
                mode=Fine.PERCENTAGE,
                percentage=2,
            ),
            interest=Interest(
                mode=Interest.MONTHLY_PERCENTAGE,
                percentage=1,
            ),
            discount=[
                Discount(
                    amount=200,
                    limit_date=pre_vencimento,
                    mode=Discount.FIXED,
                ),
            ],
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
