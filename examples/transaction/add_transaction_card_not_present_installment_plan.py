import os

from zoop_wrapper import ZoopWrapper, Transaction, Source, Token, InstallmentPlan
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

# Essa flag indica se a transação deve ser apenas pré autorizada ou capturada
capture_flag = True

# Equivalente à R$543,21
quantia_em_centavos = "54321"

t = Transaction(
    customer=seller_brian,
    description="Uma descrição breve da motivação da sua transação",
    on_behalf_of=seller_denise,
    payment_type="credit",
    statement_descriptor="Loja do Joao",
    capture=capture_flag,
    source=Source(
        card=Token(id=card_id_brian, allow_empty=True),
        usage="single_use",
        amount=quantia_em_centavos,
    ),
    installment_plan=InstallmentPlan(
        number_installments=12,
        mode="interest_free",
    ),
)

response = client.add_transaction(t)

dump_response(response, os.path.basename(__file__).split(".")[0])
