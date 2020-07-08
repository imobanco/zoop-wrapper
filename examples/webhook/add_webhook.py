import os

from zoop_wrapper import ZoopWrapper, Webhook
from examples.utils import dump_response

"""
Nesse momento as constantes podem ser criadas no arquivo .py.
Mas é recomendado utilizar como variável de ambiente em um '.env'
"""
from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY


client = ZoopWrapper(marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY)

wh = Webhook(
    description="asd",
    url="http://google.com",
    method="POST",
    events=["document.created", "document.updated"],
)


response = client.add_webhook(wh)

dump_response(response, os.path.basename(__file__).split(".")[0])
