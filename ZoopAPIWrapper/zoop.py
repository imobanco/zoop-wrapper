import requests
import json
from ZoopAPIWrapper.constants import ZOOP_KEY, MAIN_SELLER, MARKETPLACE_ID

class Zoop():
    """This class wraps the zoop API to ease use in python

    """
    def __init__(self, marketplace_id, publishable_key):
        self.BASE_ZOOP_URL = 'https://api.zoop.ws/v1/marketplaces/'

        self.marketplace_id = marketplace_id
        self.basic_auth = publishable_key


    def search_seller_by_id(self, identifier):
        url = self.BASE_ZOOP_URL + f'{MARKETPLACE_ID}/sellers/{MAIN_SELLER}'

        response = requests.get(url, auth=(ZOOP_KEY, ''))
        response_as_dict = json.loads(response.text)
        return response_as_dict
