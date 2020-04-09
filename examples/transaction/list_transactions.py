import os

from zoop_wrapper.constants import MARKETPLACE_ID, ZOOP_KEY
from zoop_wrapper.wrapper import ZoopWrapper
from examples.utils import dump_response


client = ZoopWrapper(
    marketplace_id=MARKETPLACE_ID, key=ZOOP_KEY
)

response = client.list_transactions()

dump_response(response, os.path.basename(__file__).split(".")[0])
