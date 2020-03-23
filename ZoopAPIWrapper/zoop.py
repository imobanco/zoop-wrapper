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

    def __construct_url(self, action=None, identifier=None, subaction=None, search=None):
        url = f"{self._base_url}/"
        url += f"{self.__marketplace_id}/"
        if action:
            url += f"{action}/"
        if identifier:
            url += f"{identifier}/"
        if subaction:
            url += f"{subaction}/"
        if search:
            url += f"search?{search}"
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

    def __get(self, url):
        response = requests.get(url, auth=self.__auth)
        response = self.__process_response(response)
        return response

    def __post(self, url, data):
        response = requests.post(url, data=data, auth=self.__auth)
        response = self.__process_response(response)
        return response

    def list_sellers(self):
        url = self.__construct_url(action='sellers')
        return self.__get(url)

    def retrieve_seller(self, identifier):
        url = self.__construct_url(action='sellers', identifier=identifier)
        return self.__get(url)

    def _add_seller(self, seller_type, seller):
        url = self.__construct_url(action=f'sellers/{seller_type}')
        return self.__post(url, data=seller)

    def add_individual_seller(self, seller):
        return self._add_seller('individuals', seller)

    def add_business_seller(self, seller):
        return self._add_seller('business', seller)
