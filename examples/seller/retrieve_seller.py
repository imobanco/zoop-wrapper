import os

from zoop_wrapper import ZoopWrapper
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

response = client.retrieve_seller("0e084bb6a60f47e8ac45949d5040eb92")

dump_response(response, os.path.basename(__file__).split(".")[0])
