import os

from zoop_wrapper import ZoopWrapper
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

card_transaction_id = "b8d82a6296b346f58fa02bd47b14c095"
response = client.cancel_transaction(card_transaction_id)

dump_response(response, os.path.basename(__file__).split(".")[0])
