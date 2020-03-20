import json

import requests

from ZoopAPIWrapper.constants import ZOOP_KEY, MAIN_SELLER, MARKETPLACE_ID


class Zoop:
    """This class wraps the zoop API to ease use in python

    """
    def __init__(self, ):
        self._base_url = 'https://api.zoop.ws/v1/marketplaces'

        self.__marketplace_id = MARKETPLACE_ID
        self.__key = ZOOP_KEY

    def search_seller_by_id(self, identifier):
        url = self.BASE_ZOOP_URL + f'{MARKETPLACE_ID}/sellers/{MAIN_SELLER}'

        response = requests.get(url, auth=(ZOOP_KEY, ''))
        response_as_dict = json.loads(response.text)
        return response_as_dict
