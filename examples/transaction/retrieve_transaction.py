import os

from ZoopAPIWrapper.wrapper import ZoopWrapper
from examples.utils import dump_response


client = ZoopWrapper()

response = client.retrieve_transaction('9ee5d17396bb4fdfa24bdddcb9563ca3')

dump_response(response, os.path.basename(__file__).split('.')[0])
