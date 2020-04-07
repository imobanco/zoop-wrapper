import os

from ZoopAPIWrapper.wrapper import ZoopWrapper
from ZoopAPIWrapper.models.transaction import Transaction
from ZoopAPIWrapper.models.invoice import (
    Invoice, BillingInstructions, BillingConfiguration
)
from examples.utils import dump_response


client = ZoopWrapper()

seller_id = '27e17b778b404a83bf8e25ec995e2ffe'
buyer_or_seller_id = 'e7eec0f640c14e21b35d20d58b49b584'


quantia_em_centavos = '1000'
vencimento = '2020-06-20'
limite = '2020-06-30'

t = Transaction(
    amount=quantia_em_centavos,
    description='meu boleto gerado para teste',
    on_behalf_of=seller_id,
    customer=buyer_or_seller_id,
    payment_type='boleto',
    payment_method=Invoice(
        expiration_date=vencimento,
        payment_limit_date=limite,
        billing_instructions=BillingInstructions(
            late_fee=BillingConfiguration(
                mode=BillingConfiguration.PERCENTAGE_MODE,
                percentage=50,
                start_date=vencimento
            ),
            interest=BillingConfiguration(
                mode=BillingConfiguration.MONTHLY_PERCENTAGE_MODE,
                percentage=50.5555555555,
                start_date=vencimento
            ),
            discount=BillingConfiguration(
                is_discount=True,
                mode=BillingConfiguration.FIXED_MODE,
                amount=100,
                limit_date=vencimento
            )
        )

    )
)

data = t.to_dict()
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

response = client.add_transaction(data)


dump_response(response, os.path.basename(__file__).split('.')[0])
