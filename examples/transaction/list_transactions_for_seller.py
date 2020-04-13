import os

from zoop_wrapper.wrapper import ZoopWrapper
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

response = client.list_transactions_for_seller("27e17b778b404a83bf8e25ec995e2ffe")

dump_response(response, os.path.basename(__file__).split(".")[0])
