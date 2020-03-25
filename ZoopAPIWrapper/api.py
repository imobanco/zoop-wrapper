import json

import requests

from ZoopAPIWrapper.constants import ZOOP_KEY, MARKETPLACE_ID
from ZoopAPIWrapper.models.utils import get_instance_from_data


class RequestsWrapper:
    """
    requests lib wrapper

    Attributes:
        __base_url: base url to construct requests
    """
    def __init__(self, base_url):
        self.__base_url = base_url

    def __construct_url(self, action=None, identifier=None,
                        subaction=None, search=None):
        # noinspection PyProtectedMember
        """
        construct url for the request

        Args:
            action: action endpoint
            identifier: identifier detail string (ID)
            subaction: subaction endpoint
            search: query with urls args to be researched

        Examples:
            >>> rw = RequestsWrapper()
            >>> rw._RequestsWrapper__construct_url(action='seller', identifier='1', subaction='bank_accounts', search='account_number=1')  # noqa:
            'http://zoopapiurl.com/{marketplace_id}/seller/1/bank_accounts/search?account_number=1'

        Returns: full url for the request

        """
        url = f"{self.__base_url}/"
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
        raise NotImplementedError('Must implement auth function!')

    @staticmethod
    def __process_response(response):
        response.data = json.loads(response.content)

        resource = response.data.get('resource')
        if resource == 'list':
            response.instances = [get_instance_from_data(item)
                                  for item in response.data.get('items')]
        elif resource is not None:
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

    def __delete(self, url):
        response = requests.delete(url, auth=self.__auth)
        response = self.__process_response(response)
        return response


class ZoopWrapper(RequestsWrapper):
    """
    Zoop API methods wrapper

    Attributes:
        __marketplace_id: marketplace id from zoop for the zoop account
        __key: zoop auth token
    """

    def __init__(self):
        self.__marketplace_id = MARKETPLACE_ID
        self.__key = ZOOP_KEY

        super().__init__(
            base_url=f'https://api.zoop.ws/v1/marketplaces/'
                     f'{self.__marketplace_id}'
        )

    @property
    def __auth(self):
        return self.__key, ''

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

    def _add_seller(self, seller_type, seller):
        url = self.__construct_url(action=f'sellers', subaction=seller_type)
        return self.__post(url, data=seller)

    def add_individual_seller(self, seller):
        return self._add_seller('individuals', seller)

    def add_business_seller(self, seller):
        return self._add_seller('business', seller)

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
