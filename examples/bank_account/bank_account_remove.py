import os

from zoop_wrapper import ZoopWrapper
from examples.utils import dump_response


"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

seller_brian = "0b05a360f4b749498f74e13004c08024"
brian = client.retrieve_seller(seller_brian)

response = client.remove_bank_account("e85edf6d0add48339e3d8189f615c3b1")

dump_response(response, os.path.basename(__file__).split(".")[0])
