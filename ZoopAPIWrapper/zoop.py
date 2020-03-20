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

        self.__main_seller = MAIN_SELLER

    def __construct_url(self, action=None, identifier=None):
        url = f"{self._base_url}/"
        url += f"{self.__marketplace_id}/"
        if action:
            url += f"{action}/"
        if identifier:
            url += f"{identifier}/"
        return url

        response = requests.get(url, auth=(ZOOP_KEY, ''))
        response_as_dict = json.loads(response.text)
        return response_as_dict
