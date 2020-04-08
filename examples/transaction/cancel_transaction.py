import os

from zoop_wrapper.wrapper import ZoopWrapper
from examples.utils import dump_response


client = ZoopWrapper()

card_transaction_id = '0b8361b8fdd1480783800229f87310c2'
response = client.cancel_transaction(card_transaction_id)

dump_response(response, os.path.basename(__file__).split('.')[0])
