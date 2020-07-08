import os

from zoop_wrapper import ZoopWrapper
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

webhook_id = "2ad882a6f17b4ab194295bdff17d23ad"

response = client.remove_webhook(webhook_id)

dump_response(response, os.path.basename(__file__).split(".")[0])
