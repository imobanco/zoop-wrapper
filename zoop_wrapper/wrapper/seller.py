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
            data = {
                "taxpayer_id": "foo",
                "first_name": "foo",
                "last_name": "foo",
                "email": "foo@bar.com",
                "phone_number": "+55 84 99999-9999",
                "birthdate": "1994-12-27",
                "address": {
                    "line1": "foo",
                    "line2": "123",
                    "line3": "barbar",
                    "neighborhood": "fooofoo",
                    "city": "Natal",
                    "state": "RN",
                    "postal_code": "59152250",
                    "country_code": "BR"
                }
            }

            data = {
                "business_name": "foo",
                "business_phone": "foo",
                "business_email": "foo",
                "business_website": "foo",
                "business_opening_date": "foo",
                "ein": "foo",
                "owner": {
                    "first_name": "foo",
                    "last_name": "foo",
                    "email": "foo",
                    "taxpayer_id": "foo",
                    "phone_number": "foo",
                    "birthdate": "foo",
                    "address": {
                        "line1": "foo",
                        "line2": "123",
                        "line3": "barbar",
                        "neighborhood": "fooofoo",
                        "city": "Natal",
                        "state": "RN",
                        "postal_code": "59152250",
                        "country_code": "BR"
                    }
                },
                "business_address": {
                    "line1": "foo",
                    "line2": "123",
                    "line3": "barbar",
                    "neighborhood": "fooofoo",
                    "city": "Natal",
                    "state": "RN",
                    "postal_code": "59152250",
                    "country_code": "BR"
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

    def update_seller(self, identifier: str, data: Union[dict, Seller]) -> ZoopResponse:
        """
        Atualiza um :class:`.Seller`.

        Examples:
            data = {
                "taxpayer_id": "foo",
                "first_name": "foo",
                "last_name": "foo",
                "email": "foo@bar.com",
                "phone_number": "+55 84 99999-9999",
                "birthdate": "1994-12-27",
                "address": {
                    "line1": "foo",
                    "line2": "123",
                    "line3": "barbar",
                    "neighborhood": "fooofoo",
                    "city": "Natal",
                    "state": "BR-RN",
                    "postal_code": "59152250",
                    "country_code": "BR"
                }
            }

            data = {
                "business_name": "foo",
                "business_phone": "foo",
                "business_email": "foo",
                "business_website": "foo",
                "business_opening_date": "foo",
                "ein": "foo",
                "owner": {
                    "first_name": "foo",
                    "last_name": "foo",
                    "email": "foo",
                    "taxpayer_id": "foo",
                    "phone_number": "foo",
                    "birthdate": "foo",
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
            identifier: id do :class:`.Seller`
            data: dados do :class:`.Seller`

        Returns:
            :class:`.ZoopResponse`
        """
        instance = Seller.from_dict_or_instance(data)
        url = self._construct_url(
            action=f"sellers",
            identifier=identifier,
            subaction=instance.get_type_uri(),
            sub_action_before_identifier=True,
        )
        return self._put_instance(url, instance=instance)

    def __search_seller(self, **kwargs) -> ZoopResponse:
        """
        Busca um :class:`.Seller`.

        Args:
            kwargs: dicionário de valores a serem buscados

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(action="sellers", search=kwargs)
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
