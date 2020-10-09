import os

from zoop_wrapper import ZoopWrapper, BankAccount
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)


ba = BankAccount(
    type=BankAccount.SAVING_TYPE,
    holder_name='Algum Nome',
    bank_code="237",
    routing_number="123"
)

response = client.add_bank_account(ba)

dump_response(response, os.path.basename(__file__).split(".")[0])
