from ..wrapper.base import BaseZoopWrapper
from ..models.token import Token


class CardWrapper(BaseZoopWrapper):
    """
    Card Wrapper

    Contains methods for :class:`.Card` resource
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
