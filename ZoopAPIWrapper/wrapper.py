import requests

from ZoopAPIWrapper.constants import ZOOP_KEY, MARKETPLACE_ID, LOG_LEVEL
from ZoopAPIWrapper.models.base import ZoopModel
from ZoopAPIWrapper.models.buyer import Buyer
from ZoopAPIWrapper.models.seller import Seller
from ZoopAPIWrapper.models.utils import get_instance_from_data
from ZoopAPIWrapper.utils import (
    get_logger, config_logging
)


config_logging(LOG_LEVEL)
logger = get_logger('wrapper')


class RequestsWrapper:
    """
    requests lib wrapper

    Attributes:
        __base_url: base url to construct requests
    """
    def __init__(self, base_url):
        self.__base_url = base_url

    @staticmethod
    def __process_response(response):
        """
        add 'data' attribute to response from json content.
        add 'instance' or 'instances' attribute to response by resource.
        add 'error' attribute to response if had errors

        Args:
            response: http response

        Returns: processed http response
        """
        response.data = response.json()

        deleted = response.data.get('deleted')
        if not deleted:
            resource = response.data.get('resource')
            if resource == 'list':
                response.instances = [get_instance_from_data(item)
                                      for item in response.data.get('items')]
            elif resource is not None:
                response.instance = get_instance_from_data(response.data)

        if response.data.get('error'):
            response.error = response.data.get('error').get('message')
            logger.warning(f'respose has error: {response.error}')
        return response

    def _construct_url(self, action=None, identifier=None,
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
            >>> rw._construct_url(action='seller', identifier='1', subaction='bank_accounts', search='account_number=1')  # noqa:
            'rw.__base_url/seller/1/bank_accounts/search?account_number=1'

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
    def _auth(self):
        """
        property of authentication

        Raises:
            NotImplementedError: it's a abstract method
        """
        raise NotImplementedError('Must implement auth function!')

    def _get(self, url):
        """
        http get request wrapper

        Args:
            url: url to be requested

        Returns: processed response
        """
        response = requests.get(url, auth=self._auth)
        response = self.__process_response(response)
        return response

    def _post(self, url, data):
        """
        http post request wrapper

        Args:
            url: url to be requested
            data: data to be posted

        Returns: processed response
        """
        response = requests.post(url, data=data, auth=self._auth)
        response = self.__process_response(response)
        return response

    def _delete(self, url):
        """
        http delete request wrapper

        Args:
            url: url to be requested

        Returns: processed response
        """
        response = requests.delete(url, auth=self._auth)
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
    def _auth(self):
        """
        property of authentication

        Returns: tuple with ZoopKey
        """
        return self.__key, ''

    def _post_instance(self, url, instance: ZoopModel):
        """
        http post request wrapper with instance
        
        Args:
            url: url to be requested
            instance: instance to be posted

        Returns: processed response
        """
        if not isinstance(instance, ZoopModel):
            raise TypeError('instance must be a ZoopModel')
        return self._post(url, data=instance.to_dict())

    def list_sellers(self):
        """
        list sellers
        Returns: response with instances of Seller
        """
        url = self._construct_url(action='sellers')
        return self._get(url)

    def retrieve_seller(self, identifier):
        """
        retrieve seller

        Args:
            identifier: uuid id

        Returns: response with instance of Seller
        """
        url = self._construct_url(action='sellers', identifier=identifier)
        return self._get(url)

    def list_seller_bank_accounts(self, identifier):
        """
        list all bank accounts of some seller

        Args:
            identifier: uuid id

        Returns: response with instances of BankAccount
        """
        url = self._construct_url(action='sellers',
                                  identifier=identifier,
                                  subaction='bank_accounts')
        return self._get(url)

    def _search_seller(self, id_type, identifier):
        """
        search seller

        Args:
            id_type: 'taxpayer_id' or 'ein'
            identifier: value of identifier

        Returns: response with instance of Seller
        """
        url = self._construct_url(action='sellers',
                                  search=f"{id_type}={identifier}")
        return self._get(url)

    def search_business_seller(self, identifier):
        """
        search seller by CNPJ

        Args:
            identifier: ein (Employer Identification Number) is equivalent to CNPJ  # noqa:

        Returns: response with instance of Seller
        """
        return self._search_seller('ein', identifier)

    def search_individual_seller(self, identifier):
        """
        search seller by CPF

        Args:
            identifier: taxpayer_id is equivalent to CPF  # noqa:

        Returns: response with instance of Seller
        """
        return self._search_seller('taxpayer_id', identifier)

    def add_seller(self, data: dict):
        """
        add seller

        Args:
            data: dict of data

        Returns: response with instance of Seller
        """
        instance = Seller.from_dict(data)
        url = self._construct_url(action='sellers',
                                  subaction=instance.get_type())
        return self._post_instance(url, instance=instance)

    def remove_seller(self, identifier):
        """
        remove seller

        Args:
            identifier: uuid id

        Returns: response without instance
        """
        url = self._construct_url(action='sellers', identifier=identifier)
        return self._delete(url)

    def list_bank_accounts(self):
        """
        list all bank accounts
        Returns: response with instances of BankAccount
        """
        url = self._construct_url(action='bank_accounts')
        return self._get(url)

    def retrieve_bank_account(self, identifier):
        """
        retrieve bank account

        Args:
            identifier: uuid id

        Returns: response with instance of BankAccount
        """
        url = self._construct_url(action='bank_accounts',
                                  identifier=identifier)
        return self._get(url)

    def __get_buyers(self, action='buyers', identifier=None, search=None):
        """
        get method for buyers actions

        Args:
            action: 'buyers' by default
            identifier: identifier value
            search: search value

        Returns: response with instance or instances of Buyer
        """
        url = self._construct_url(action=action,
                                  identifier=identifier,
                                  search=search)
        return self._get(url)

    def list_buyers(self):
        """
        list all buyers
        Returns: response with instances of Buyer
        """
        return self.__get_buyers()

    def retrieve_buyer(self, identifier):
        """
        retrieve buyer

        Args:
            identifier: uuid id


        Returns: response with instance of Buyer
        """
        return self.__get_buyers(identifier=identifier)

    def search_buyer(self, identifier):
        """
        search buyer

        Args:
            identifier: CPF or CNPJ

        Returns: response with instance of Buyer
        """
        return self.__get_buyers(search=f'taxpayer_id={identifier}')

    def add_buyer(self, data: dict):
        """
        add buyer

        Args:
            data: dict of data

        Returns: response with instance of Buyer
        """
        instance = Buyer.from_dict(data)
        url = self._construct_url(action='buyers')
        return self._post_instance(url, instance=instance)

    def remove_buyer(self, identifier):
        """
        remove buyer

        Args:
            identifier: uuid id

        Returns: response without instance
        """
        url = self._construct_url(action='buyers',
                                  identifier=identifier)
        return self._delete(url)
