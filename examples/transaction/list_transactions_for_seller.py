import os

from ZoopAPIWrapper.wrapper import ZoopWrapper
from examples.utils import dump_response


client = ZoopWrapper()

response = client.list_transactions_for_seller(
    '27e17b778b404a83bf8e25ec995e2ffe')

dump_response(response, os.path.basename(__file__).split('.')[0])
