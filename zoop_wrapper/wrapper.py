import requests

from zoop_wrapper.constants import ZOOP_KEY, MARKETPLACE_ID, LOG_LEVEL
from zoop_wrapper.models.base import ResourceModel
from zoop_wrapper.models.bank_account import BankAccount
from zoop_wrapper.models.buyer import Buyer
from zoop_wrapper.models.seller import Seller
from zoop_wrapper.models.token import Token
from zoop_wrapper.models.transaction import Transaction
from zoop_wrapper.models.utils import get_instance_from_data
from zoop_wrapper.utils import get_logger, config_logging


config_logging(LOG_LEVEL)
logger = get_logger("wrapper")


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
        add 'data' attribute to response from json content of response.

        add 'instance' or 'instances' attribute to response by resource.
        Only add 'instance' or 'instances' if there's no `deleted` attribute
        which is set on all delete response (200 ok) and if there's the
        `resource` attribute on response

        add 'error' attribute to response if had errors

        Args:
            response: http response

        Raises:
            HttpError: when response is not ok!

        Returns:
            processed http response
        """
        response.data = response.json()

        deleted = response.data.get("deleted")
        if not deleted:
            resource = response.data.get("resource")
            if resource == "list":
                response.instances = [
                    get_instance_from_data(item) for item in response.data.get("items")
                ]
            elif resource is not None:
                response.instance = get_instance_from_data(response.data)

        if response.data.get("error"):
            response.reason = f"{response.data.get('error').get('message')}"
            reasons = response.data.get("error").get("reasons")
            if reasons:
                response.reason += f" {reasons}"

        response.raise_for_status()
        return response

    def _construct_url(self, action=None, identifier=None, subaction=None, search=None):
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

        Returns:
            full url for the request
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
        raise NotImplementedError("Must implement auth function!")

    def _get(self, url):
        """
        http get request wrapper

        Args:
            url: url to be requested

        Returns:
            processed response
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

        Returns:
            processed response
        """
        response = requests.post(url, json=data, auth=self._auth)
        response = self.__process_response(response)
        return response

    def _delete(self, url):
        """
        http delete request wrapper

        Args:
            url: url to be requested

        Returns:
            processed response
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

    BASE_URL = "https://api.zoop.ws/v1/marketplaces/"

    def __init__(self, marketplace_id=None, key=None):
        if marketplace_id is None:
            marketplace_id = MARKETPLACE_ID

        if key is None:
            key = ZOOP_KEY

        self.__marketplace_id = marketplace_id
        self.__key = key

        super().__init__(base_url=f"{self.BASE_URL}{self.__marketplace_id}")

    @property
    def _auth(self):
        """
        property of authentication

        Returns:
            tuple with ZoopKey
        """
        return self.__key, ""

    def _post_instance(self, url, instance: ResourceModel):
        """
        http post request wrapper with instance

        Args:
            url: url to be requested
            instance: instance to be posted

        Returns:
            processed response
        """
        if not isinstance(instance, ResourceModel):
            raise TypeError("instance must be a ZoopModel")
        return self._post(url, data=instance.to_dict())

    def list_sellers(self):
        """
        list sellers

        Returns:
            response with instances of Seller
        """
        url = self._construct_url(action="sellers")
        return self._get(url)

    def retrieve_seller(self, identifier):
        """
        retrieve seller

        Args:
            identifier: uuid id

        Returns:
            response with instance of Seller
        """
        url = self._construct_url(action="sellers", identifier=identifier)
        return self._get(url)

    def list_seller_bank_accounts(self, identifier):
        """
        list all bank accounts of some seller

        Args:
            identifier: uuid id

        Returns:
            response with instances of BankAccount
        """
        url = self._construct_url(
            action="sellers", identifier=identifier, subaction="bank_accounts"
        )
        return self._get(url)

    def _search_seller(self, id_type, identifier):
        """
        search seller

        Args:
            id_type: 'taxpayer_id' or 'ein'
            identifier: value of identifier

        Returns:
            response with instance of Seller
        """
        url = self._construct_url(action="sellers", search=f"{id_type}={identifier}")
        return self._get(url)

    def search_business_seller(self, identifier):
        """
        search seller by CNPJ

        Args:
            identifier: ein (Employer Identification Number) is equivalent to CNPJ  # noqa:

        Returns:
            response with instance of Seller
        """
        return self._search_seller("ein", identifier)

    def search_individual_seller(self, identifier):
        """
        search seller by CPF

        Args:
            identifier: taxpayer_id is equivalent to CPF  # noqa:

        Returns:
            response with instance of Seller
        """
        return self._search_seller("taxpayer_id", identifier)

    def add_seller(self, data: dict):
        """
        add seller

        Examples:
            data = {
                'taxpayer_id': 'foo',
                'first_name': 'foo',
                'last_name': 'foo',
                'email': 'foo@bar.com',
                'phone_number': '+55 84 99999-9999',
                'birthdate': '1994-12-27',
                'address': {
                    'line1': 'foo',
                    'line2': '123',
                    'line3': 'barbar',
                    'neighborhood': 'fooofoo',
                    'city': 'Natal',
                    'state': 'BR-RN',
                    'postal_code': '59152250',
                    'country_code': "BR"
                }
            }

            data = {
                "business_name": "foo",
                "business_phone": "foo",
                "business_email": "foo",
                "business_website": "foo",
                "business_opening_date": "foo",
                "ein": "foo",
                'owner': {
                    "first_name": "foo",
                    "last_name": "foo",
                    "email": "foo",
                    "taxpayer_id": "foo",
                    "phone_number": "foo",
                    "birthdate": 'foo',
                    "address": {
                        "line1": "foo",
                        "line2": "foo",
                        "line3": "foo",
                        "neighborhood": "foo",
                        "city": "foo",
                        "state": "foo",
                        "postal_code": "foo",
                        "country_code": "foo"
                    }
                }
                "business_address": {
                    "line1": "foo",
                    "line2": "foo",
                    "line3": "foo",
                    "neighborhood": "foo",
                    "city": "foo",
                    "state": "foo",
                    "postal_code": "foo",
                    "country_code": "foo"
                }
            }

        Args:
            data: dict of data

        Returns:
            response with instance of Seller
        """
        instance = Seller.from_dict_or_instance(data)
        url = self._construct_url(action="sellers", subaction=instance.get_type_uri())
        return self._post_instance(url, instance=instance)

    def remove_seller(self, identifier):
        """
        remove seller

        Args:
            identifier: uuid id

        Returns:
            response without instance
        """
        url = self._construct_url(action="sellers", identifier=identifier)
        return self._delete(url)

    def list_bank_accounts(self):
        """
        list all bank accounts

        Returns:
            response with instances of BankAccount
        """
        url = self._construct_url(action="bank_accounts")
        return self._get(url)

    def retrieve_bank_account(self, identifier):
        """
        retrieve bank account

        Args:
            identifier: uuid id

        Returns:
            response with instance of BankAccount
        """
        url = self._construct_url(action="bank_accounts", identifier=identifier)
        return self._get(url)

    def __add_bank_account_token(self, token: Token):
        """
        add bank account token

        Args:
            token: Token instance for BankAccount

        Returns:
            response with instance of Token
        """
        url = self._construct_url(action="bank_accounts", subaction="tokens")
        return self._post_instance(url, instance=token)

    def add_bank_account(self, data: dict):
        """
        add bank account

        Examples:
            data = {
                'taxpayer_id' or 'ein': 'foo',
                'holder_name': 'foo',
                'bank_code': 'foo',
                'routing_number': 'foo',
                'account_number': 'foo',
                'type': 'foo'
            }

        Args:
            data: dict of data

        Returns:
            response with instance of BankAccount
        """
        instance = Token.from_dict_or_instance(data)

        bank_account_type = instance.get_bank_account_type()
        if bank_account_type == BankAccount.INDIVIDUAL_TYPE:
            seller_response = self.search_individual_seller(instance.taxpayer_id)
        elif bank_account_type == BankAccount.BUSINESS_TYPE:
            seller_response = self.search_business_seller(instance.ein)
        else:
            raise TypeError("this is not supposed to happen!")

        seller_instance = seller_response.instance

        token_response = self.__add_bank_account_token(instance)
        created_token = token_response.instance

        data = {"customer": seller_instance.id, "token": created_token.id}

        url = self._construct_url(action="bank_accounts")
        return self._post(url, data=data)

    def list_buyers(self):
        """
        list all buyers

        Returns:
            response with instances of Buyer
        """
        url = self._construct_url(action="buyers")
        return self._get(url)

    def retrieve_buyer(self, identifier):
        """
        retrieve buyer

        Args:
            identifier: uuid id

        Returns:
            response with instance of Buyer
        """
        url = self._construct_url(action="buyers", identifier=identifier)
        return self._get(url)

    def search_buyer(self, identifier):
        """
        search buyer by CPF or CNPJ.
        Yes, the name of the attribute is taxpayer_id for
        both.

        Args:
            identifier: CPF or CNPJ

        Returns:
            response with instance of Buyer
        """
        url = self._construct_url(action="buyers", search=f"taxpayer_id={identifier}")
        return self._get(url)

    def add_buyer(self, data: dict):
        """
        add buyer

        Examples:
            data = {
                "first_name": "foo",
                "last_name": "foo",
                "email": "foo",
                "taxpayer_id": "foo",
                "phone_number": "foo",
                "birthdate": 'foo',
                "address": {
                    "line1": "foo",
                    "line2": "foo",
                    "line3": "foo",
                    "neighborhood": "foo",
                    "city": "foo",
                    "state": "foo",
                    "postal_code": "foo",
                    "country_code": "foo"
                }
            }

        Args:
            data: dict of data

        Returns:
            response with instance of Buyer
        """
        instance = Buyer.from_dict_or_instance(data)
        url = self._construct_url(action="buyers")
        return self._post_instance(url, instance=instance)

    def remove_buyer(self, identifier):
        """
        remove buyer

        Args:
            identifier: uuid id

        Returns:
            response without instance
        """
        url = self._construct_url(action="buyers", identifier=identifier)
        return self._delete(url)

    def list_transactions(self):
        """
        list all transactions

        Returns:
            response
        """
        url = self._construct_url(action="transactions")
        return self._get(url)

    def list_transactions_for_seller(self, identifier):
        """
        list all transactions from seller

        Args:
            identifier: uuid id

        Returns:
            response
        """
        url = self._construct_url(
            action="sellers", identifier=identifier, subaction="transactions"
        )
        return self._get(url)

    def retrieve_transaction(self, identifier):
        """
        retrieve a transaction

        Args:
            identifier: uuid id

        Returns:
            response
        """
        url = self._construct_url(action="transactions", identifier=identifier)
        return self._get(url)

    def add_transaction(self, data: dict):
        """
        add transaction

        Examples:
            data = {
                'amount' : 'foo',
                'currency' : 'BRL',
                'description' : 'foo',
                'reference_id' : 'foo',
                'on_behalf_of' : 'foo',
                'customer': 'foo',
                'payment_type' : 'foo',
                'payment_method' : {
                    'expiration_date' : expiration_date,
                    'payment_limit_date' : payment_limit_date,
                    'body_instructions' : instructions,
                    'billing_instructions' : {
                        'late_fee' : late_fee,
                        'interest' : interest,
                        'discount' : discount
                    }
                }
            }

            data = {
                'amount': '1000',
                'currency': 'BRL',
                'description': 'meu boleto gerado para teste',
                'on_behalf_of': 'seller_id',
                'customer': 'buyer_id',
                'payment_type': 'boleto',
                'payment_method': {
                    'expiration_date': '2020-06-20',
                    'payment_limit_date': '2020-06-30',
                    'billing_instructions': {
                        'late_fee': {
                            'mode': 'FIXED',
                            'percentage': 30,
                            'start_date': '2020-06-20'
                        },
                        'interest': {
                            'mode': 'MONTHLY_PERCENTAGE',
                            'percentage': 30,
                            'start_date': '2020-06-20'
                        },
                        'discount': [{
                            'mode': 'FIXED',
                            'amount': 300,
                            'limit_date': '2020-06-20'
                        }]
                    }
                }
            }

        Args:
            data: dict of data

        Returns:
            response with instance of Transaction
        """
        instance = Transaction.from_dict_or_instance(data)
        url = self._construct_url(action="transactions")
        return self._post_instance(url, instance=instance)

    def cancel_transaction(self, identifier):
        """
        cancel a transaction

        Args:
            identifier: uuid id

        Returns:
            response
        """
        # @TODO: terminar de testar cancel transaction (card transaction)
        url = self._construct_url(
            action="transactions", identifier=identifier, subaction="void"
        )
        return self._get(url)

    def retrieve_invoice(self, identifier):
        """
        retrieve invoice

        Args:
            identifier: uuid id

        Returns:
            response with instance of Invoice
        """
        url = self._construct_url(action="boletos", identifier=identifier)
        return self._get(url)

    def retrieve_card(self, identifier):
        """
        retrieve card

        Args:
            identifier: uuid id

        Returns:
            response without instance
        """
        url = self._construct_url(action="cards", identifier=identifier)
        return self._get(url)

    def __add_card_token(self, card_token: Token):
        """
        add card token

        Args:
            card_token: Token instance for Card

        Returns:
            response with instance of Token
        """
        url = self._construct_url(action="cards", subaction="tokens")
        return self._post_instance(url, instance=card_token)

    def add_card(self, data: dict, buyer_identifier):
        """
        add card

        Examples:
            data = {
                "holder_name": "foo",
                "expiration_month": "foo",
                "expiration_year": "foo",
                "card_number": "foo",
                "security_code": "foo"
            }

        Args:
            data: dict of data
            buyer_identifier: uuid of buyer

        Returns:
            response with instance of BankAccount
        """
        token = Token.from_dict_or_instance(data)

        buyer_response = self.retrieve_buyer(buyer_identifier)
        buyer_instance = buyer_response.instance

        token_response = self.__add_card_token(token)
        created_token = token_response.instance

        data = {"customer": buyer_instance.id, "token": created_token.id}

        url = self._construct_url(action="cards")
        return self._post(url, data=data)
