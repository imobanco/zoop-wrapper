from ..wrapper.base import BaseZoopWrapper
from ..models.buyer import Buyer


class BuyerWrapper(BaseZoopWrapper):
    """
    Possui os métodos do resource :class:`.Buyer`
    """

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
