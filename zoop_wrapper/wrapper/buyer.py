from typing import Union

from .base import BaseZoopWrapper
from ..models.buyer import Buyer
from ..response import ZoopResponse


class BuyerWrapper(BaseZoopWrapper):
    """
    Possui os métodos do resource :class:`.Buyer`
    """

    def add_buyer(self, data: Union[dict, Buyer]) -> ZoopResponse:
        """
        Adiciona um :class:`.Buyer`

        Examples:
            >>> data = {
                "birthdate": 'foo',
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

        Args:
            data (dict ou :class:`.Buyer`): dados do :class:`.Buyer`

        Returns:
            :class:`.ZoopResponse`
        """
        instance = Buyer.from_dict_or_instance(data)
        url = self._construct_url(action="buyers")
        return self._post_instance(url, instance=instance)

    def list_buyers(self) -> ZoopResponse:
        """
        Lista todos os :class:`.Buyer`'s

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(action="buyers")
        return self._get(url)

    def retrieve_buyer(self, identifier: str) -> ZoopResponse:
        """
        Pega um :class:`.Buyer`

        Args:
            identifier: uuid id

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(action="buyers", identifier=identifier)
        return self._get(url)

    def remove_buyer(self, identifier: str) -> ZoopResponse:
        """
        Remove um :class:`.Buyer`

        Args:
            identifier: uuid id

        Returns:
           :class:`.ZoopResponse`
        """
        url = self._construct_url(action="buyers", identifier=identifier)
        return self._delete(url)

    def search_buyer(self, identifier: str) -> ZoopResponse:
        """
        Buscar um :class:`.Buyer` pelo CPF ou CNPJ

        .. note::
            Sim, o atributo é o :attr:`.taxpayer_id` para os dois.
            Veja o código para entender.

        Args:
            identifier: CPF ou CNPJ

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(
            action="buyers/search", search=f"taxpayer_id={identifier}"
        )
        return self._get(url)

    def update_buyer(self, identifier: str, data: Union[dict, Buyer]) -> ZoopResponse:
        """
        Atualiza um :class:`.Buyer`.

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

        Args:
            identifier: id do :class:`.Buyer`
            data: dados do :class:`.Buyer`

        Returns:
            :class:`.ZoopResponse`
        """
        instance = Buyer.from_dict_or_instance(data)
        url = self._construct_url(action="buyers", identifier=identifier)
        return self._put_instance(url, instance=instance)
