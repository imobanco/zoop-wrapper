import os

from zoop_wrapper import ZoopWrapper, BankAccount
from examples.utils import dump_response

from examples.transaction.add_transaction_card_present import seller_brian

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

brian = client.retrieve_seller(seller_brian)

ba = {
    "account_number": "123",
    "bank_code": "237",
    "holder_name": "Algum Nome",
    "routing_number": "foo",
    "taxpayer_id": brian.instance.taxpayer_id,
    "type": BankAccount.SAVING_TYPE,
}


response = client.add_bank_account(ba)

dump_response(response, os.path.basename(__file__).split(".")[0])
