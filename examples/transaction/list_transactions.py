import os

from ZoopAPIWrapper.wrapper import ZoopWrapper
from examples.utils import dump_response


client = ZoopWrapper()

response = client.list_transactions()

dump_response(response, os.path.basename(__file__).split('.')[0])