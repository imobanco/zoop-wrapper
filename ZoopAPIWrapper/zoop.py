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

    @property
    def __auth(self):
        return ZOOP_KEY, ''

    @staticmethod
    def __process_response(response):
        response.data = json.loads(response.content)
        if response.data.get('error'):
            response.error = response.data.get('error').get('message')
        return response
