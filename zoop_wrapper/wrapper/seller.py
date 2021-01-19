from typing import Union

from .base import BaseZoopWrapper
from ..response import ZoopResponse
from ..models.seller import Seller


class SellerWrapper(BaseZoopWrapper):
    """
    Possui os métodos do resource :class:`.Seller`
    """

    def add_seller(self, data: Union[dict, Seller]) -> ZoopResponse:
        """
        Adiciona um :class:`.Seller`.

        Examples:
            >>> data = {
                "birthdate": "1994-12-27",
                "email": "foo@bar.com",
                "first_name": "foo",
                "last_name": "foo",
                "phone_number": "+55 84 99999-9999",
                "taxpayer_id": "foo",
                "address": {
                    "city": "Natal",
                    "country_code": "BR"
                    "line1": "foo",
                    "line2": "123",
                    "line3": "barbar",
                    "neighborhood": "fooofoo",
                    "postal_code": "59152250",
                    "state": "RN",
                }
            }

            >>> data = {
                "business_email": "foo",
                "business_name": "foo",
                "business_opening_date": "foo",
                "business_phone": "foo",
                "business_website": "foo",
                "ein": "foo",
                "owner": {
                    "birthdate": "foo",
                    "email": "foo",
                    "first_name": "foo",
                    "last_name": "foo",
                    "phone_number": "foo",
                    "taxpayer_id": "foo",
                    "address": {
                        "city": "Natal",
                        "country_code": "BR"
                        "line1": "foo",
                        "line2": "123",
                        "line3": "barbar",
                        "neighborhood": "fooofoo",
                        "postal_code": "59152250",
                        "state": "RN",
                    }
                },
                "business_address": {
                    "city": "Natal",
                    "country_code": "BR"
                    "line1": "foo",
                    "line2": "123",
                    "line3": "barbar",
                    "neighborhood": "fooofoo",
                    "postal_code": "59152250",
                    "state": "RN",
                }
            }

        Args:
            data: dados do :class:`.Seller`

        Returns:
            :class:`.ZoopResponse`
        """
        instance = Seller.from_dict_or_instance(data)
        url = self._construct_url(action="sellers", subaction=instance.get_type_uri())
        return self._post_instance(url, instance=instance)

    def list_sellers(self) -> ZoopResponse:
        """
        lista :class:`.Seller`"s existentes na Zoop.

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(action="sellers")
        return self._get(url)

    def list_seller_bank_accounts(self, identifier: str) -> ZoopResponse:
        """
        Lista :class:`.BankAccount`"s de algum :class:`.Seller`

        Args:
            identifier: id do :class:`.Seller`

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(
            action="sellers", identifier=identifier, subaction="bank_accounts"
        )
        return self._get(url)

    def retrieve_seller(self, identifier: str) -> ZoopResponse:
        """
        Pega um :class:`.Seller`

        Args:
            identifier: id do :class:`.Seller`

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(action="sellers", identifier=identifier)
        return self._get(url)

    def remove_seller(self, identifier: str) -> ZoopResponse:
        """
        Remove um :class:`.Seller`;

        Args:
            identifier: id do :class:`.Seller`

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(action="sellers", identifier=identifier)
        return self._delete(url)

    def __search_seller(self, **kwargs) -> ZoopResponse:
        """
        Busca um :class:`.Seller`.

        Args:
            kwargs: dicionário de valores a serem buscados

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(action="sellers/search", search=kwargs)
        return self._get(url)

    def search_business_seller(self, identifier: str) -> ZoopResponse:
        """
        search seller by CNPJ

        Args:
            identifier: ein (Employer Identification Number) is equivalent to CNPJ  # noqa:

        Returns:
            response with instance of Seller
        """
        return self.__search_seller(ein=identifier)

    def search_individual_seller(self, identifier: str) -> ZoopResponse:
        """
        search seller by CPF

        Args:
            identifier: taxpayer_id is equivalent to CPF  # noqa:

        Returns:
            response with instance of Seller
        """
        return self.__search_seller(taxpayer_id=identifier)

    def update_seller(self, identifier: str, data: Union[dict, Seller]) -> ZoopResponse:
        """
        Atualiza um :class:`.Seller`.

        Examples:
            >>> data = {
                "birthdate": "1994-12-27",
                "email": "foo@bar.com",
                "first_name": "foo",
                "last_name": "foo",
                "phone_number": "+55 84 99999-9999",
                "taxpayer_id": "foo",
                "address": {
                    "city": "Natal",
                    "country_code": "BR"
                    "line1": "foo",
                    "line2": "123",
                    "line3": "barbar",
                    "neighborhood": "fooofoo",
                    "postal_code": "59152250",
                    "state": "BR-RN",
                }
            }

            >>> data = {
                "business_email": "foo",
                "business_name": "foo",
                "business_opening_date": "foo",
                "business_phone": "foo",
                "business_website": "foo",
                "ein": "foo",
                "owner": {
                    "birthdate": "foo",
                    "email": "foo",
                    "first_name": "foo",
                    "last_name": "foo",
                    "phone_number": "foo",
                    "taxpayer_id": "foo",
                    "address": {
                        "city": "foo",
                        "country_code": "foo"
                        "line1": "foo",
                        "line2": "foo",
                        "line3": "foo",
                        "neighborhood": "foo",
                        "postal_code": "foo",
                        "state": "foo",
                    }
                }
                "business_address": {
                    "city": "foo",
                    "country_code": "foo"
                    "line1": "foo",
                    "line2": "foo",
                    "line3": "foo",
                    "neighborhood": "foo",
                    "postal_code": "foo",
                    "state": "foo",
                }
            }

        Args:
            identifier: id do :class:`.Seller`
            data: dados do :class:`.Seller`

        Returns:
            :class:`.ZoopResponse`
        """
        instance = Seller.from_dict_or_instance(data)
        url = self._construct_url(
            action="sellers",
            identifier=identifier,
            subaction=instance.get_type_uri(),
            sub_action_before_identifier=True,
        )
        return self._put_instance(url, instance=instance)
