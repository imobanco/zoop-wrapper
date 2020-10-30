from typing import Union

from requests import HTTPError

from .base import BaseZoopWrapper
from ..exceptions import ValidationError, FieldError
from ..models.token import Token


class CardWrapper(BaseZoopWrapper):
    """
    Possui os métodos do resource :class:`.Card`

    .. warning:: Não importe isso diretamente!

        Essa classe precisa de métodos presentes em outro wrapper
    """

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
        Cria um :class:`.Token` do tipo :class:`.Card`

        Args:
            card_token: instância do :class:`.Token`

        Returns:
            :class:`.ZoopResponse` com instância do :class:`.Token`
        """
        url = self._construct_url(action="cards", subaction="tokens")
        return self._post_instance(url, instance=card_token)

    def add_card(self, data: Union[dict, Token], customer_identifier: str):
        """
        Adiciona um cartão de crédito utilizando um Token de cartão de crédito

        Examples:
            >>> data = {
                "card_number": "foo",
                "expiration_month": "foo",
                "expiration_year": "foo",
                "holder_name": "foo",
                "security_code": "foo"
            }

        Args:
            data: dicionário de dados
            customer_identifier: uuid do consumidor (:class:`.Buyer` ou :class:`.Seller`)  # noqa

        Returns:
            :class:`.ZoopResponse` com instância do :class:`.Card`
        """
        token = Token.from_dict_or_instance(data)

        try:
            self.retrieve_buyer(customer_identifier)  # type: ignore
        except HTTPError:
            try:
                self.retrieve_seller(customer_identifier)  # type: ignore
            except HTTPError:
                raise ValidationError(
                    self,
                    FieldError(
                        "customer_identifier",
                        "Não existe Seller ou Buyer para esse identificador",
                    ),
                )

        token_response = self.__add_card_token(token)
        created_token = token_response.data

        data = {"customer": customer_identifier, "token": created_token["id"]}

        url = self._construct_url(action="cards")
        return self._post(url, data=data)
