import json

import requests

from ZoopAPIWrapper.constants import ZOOP_KEY, MAIN_SELLER, MARKETPLACE_ID
from ZoopAPIWrapper.models.base import ZoopModel
from ZoopAPIWrapper.models.utils import get_instance_from_data
from ZoopAPIWrapper.models.seller import Seller
from ZoopAPIWrapper.models.bank_account import (
    BankAccount, IndividualBankAccount, BusinessBankAccount)
from ZoopAPIWrapper.models.token import Token


class Zoop:
    """
    This class wraps the zoop API to ease use in python
    """

    def __init__(self):
        self._base_url = 'https://api.zoop.ws/v1/marketplaces'

        self.__marketplace_id = MARKETPLACE_ID
        self.__key = ZOOP_KEY

        self.__main_seller = MAIN_SELLER

    def __construct_url(self, action=None, identifier=None,
                        subaction=None, search=None):
        """
        construct url for the request

        Args:
            action: action endpoint
            identifier: identifier detail string (ID)
            subaction: subaction endpoint
            search: query with urls args to be researched

        Examples:
            >>> zoop = Zoop()
            >>> zoop._Zoop__construct_url(action='seller', identifier='1', subaction='bank_accounts', search='account_number=1')  # noqa:
            'http://zoopapiurl.com/{marketplace_id}/seller/1/bank_accounts/search?account_number=1'

        Returns: full url for the request

        """
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
        if response.data.get('resource'):
            if response.data.get('resource') == 'list':
                response.instances = [get_instance_from_data(item)
                                      for item in response.data.get('items')]
            else:
                response.instance = get_instance_from_data(response.data)
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

    def __post_instance(self, url, instance: ZoopModel):
        if not isinstance(instance, ZoopModel):
            raise TypeError('instance must be a ZoopModel')
        return self.__post(url, data=instance.to_dict())

    def __delete(self, url):
        response = requests.delete(url, auth=self.__auth)
        response = self.__process_response(response)
        return response

    def list_sellers(self):
        url = self.__construct_url(action='sellers')
        return self.__get(url)

    def retrieve_seller(self, identifier):
        url = self.__construct_url(action='sellers', identifier=identifier)
        return self.__get(url)

    def _search_seller(self, id_type, identifier):
        url = self.__construct_url(action='sellers',
                                   search=f"{id_type}={identifier}")
        return self.__get(url)

    def search_business_seller(self, identifier):
        """
        search business by CNPJ
        Args:
            identifier: ein (Employer Identification Number) is equivalent to CNPJ  # noqa:

        Returns: response with Seller
        """
        return self._search_seller('ein', identifier)

    def search_individual_seller(self, identifier):
        return self._search_seller('taxpayer_id', identifier)

    def add_seller(self, data: dict):
        seller_instance = Seller.from_dict(data)
        assert isinstance(seller_instance, Seller)
        url = self.__construct_url(action=f'sellers',
                                   subaction=seller_instance.type)
        return self.__post_instance(url, instance=seller_instance)

    def remove_seller(self, identifier):
        url = self.__construct_url(action='sellers', identifier=identifier)
        return self.__delete(url)

    def list_bank_accounts(self):
        url = self.__construct_url(action='bank_accounts')
        return self.__get(url)

    def list_seller_bank_accounts(self, identifier):
        url = self.__construct_url(action='sellers',
                                   identifier=identifier,
                                   subaction='bank_accounts')
        return self.__get(url)

    def retrieve_bank_account(self, identifier):
        url = self.__construct_url(action='bank_accounts',
                                   identifier=identifier)
        return self.__get(url)
