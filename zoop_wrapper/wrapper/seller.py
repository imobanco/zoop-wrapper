from ..wrapper.base import BaseZoopWrapper
from ..models.seller import Seller


class SellerWrapper(BaseZoopWrapper):
    """
    Seller Wrapper

    Contains methods for :class:`.Seller` resource
    """

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
