from .base import BaseZoopWrapper
from ..models.buyer import Buyer


class BuyerWrapper(BaseZoopWrapper):
    """
    Possui os métodos do resource :class:`.Buyer`
    """

    def list_buyers(self):
        """
        Lista todos os :class:`.Buyer`'s

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(action="buyers")
        return self._get(url)

    def retrieve_buyer(self, identifier):
        """
        Pega um :class:`.Buyer`

        Args:
            identifier: uuid id

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(action="buyers", identifier=identifier)
        return self._get(url)

    def search_buyer(self, identifier):
        """
        Buscar um :class:`.Buyer` pelo CPF ou CNPJ

        .. note::
            Sim, o atributo é o :attr:`.taxpayer_id` para os dois. Veja o código para entender.

        Args:
            identifier: CPF ou CNPJ

        Returns:
            :class:`.ZoopResponse`
        """
        url = self._construct_url(action="buyers", search=f"taxpayer_id={identifier}")
        return self._get(url)

    def add_buyer(self, data: dict):
        """
        Adiciona um :class:`.Buyer`

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
            data (dict ou :class:`.Buyer`): dados do :class:`.Buyer`

        Returns:
            :class:`.ZoopResponse`
        """
        instance = Buyer.from_dict_or_instance(data)
        url = self._construct_url(action="buyers")
        return self._post_instance(url, instance=instance)

    def remove_buyer(self, identifier):
        """
        Remove um :class:`.Buyer`

        Args:
            identifier: uuid id

        Returns:
           :class:`.ZoopResponse`
        """
        url = self._construct_url(action="buyers", identifier=identifier)
        return self._delete(url)
