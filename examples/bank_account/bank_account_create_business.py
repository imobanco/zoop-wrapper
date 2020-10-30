import os

from zoop_wrapper import ZoopWrapper, BankAccount
from examples.utils import dump_response


"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

business_seller_id = "ef90df686ab64e6cbcdc2c1d68156605"
response = client.retrieve_seller(business_seller_id)

ba = {
    "account_number": "123123",
    "bank_code": "001",
    "holder_name": "Algum Nome",
    "routing_number": "123123",
    "ein": response.data["ein"],
    "type": BankAccount.SAVING_TYPE,
}

response = client.add_bank_account(ba)

dump_response(response, os.path.basename(__file__).split(".")[0])
