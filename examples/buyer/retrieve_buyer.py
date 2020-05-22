import os

from zoop_wrapper import ZoopWrapper
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

buyer_id = "ffe4b7a1f19c4a9da85b6d72c0b6201c"

response = client.retrieve_buyer(buyer_id)

dump_response(response, os.path.basename(__file__).split(".")[0])
