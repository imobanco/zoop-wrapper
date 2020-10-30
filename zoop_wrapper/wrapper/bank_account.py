from .base import BaseZoopWrapper
from ..models.bank_account import BankAccount
from ..models.token import Token


class BankAccountWrapper(BaseZoopWrapper):
    """
    Possui os métodos do resource :class:`.BankAccount`

    .. warning:: Não importe isso diretamente!

        Essa classe precisa de métodos presentes em outro wrapper
    """

    def list_bank_accounts_by_seller(self, identifier):
        """
        Lista todas as :class:`.BankAccount`'s.

        Returns:
            response with instances of :class:`.BankAccount`
        """
        url = self._construct_url(
            action="sellers", identifier=identifier, subaction="bank_accounts"
        )
        return self._get(url)

    def retrieve_bank_account(self, identifier):
        """
        Retorna uma :class:`.BankAccount`.

        Args:
            identifier: uuid id da :class:`.BankAccount`

        Returns:
            response with instance of :class:`.BankAccount`
        """
        url = self._construct_url(action="bank_accounts", identifier=identifier)
        return self._get(url)

    def __add_bank_account_token(self, token: Token):
        """
        Adiciona um :class:`.Token` para uma :class:`.BankAccount`.

        Args:
            token: :class:`.Token` para :class:`.BankAccount`.

        Returns:
            response with instance of  :class:`.Token`
        """
        url = self._construct_url(action="bank_accounts", subaction="tokens")
        return self._post_instance(url, instance=token)

    def add_bank_account(self, data: dict):
        """
        Adiciona uma :class:`.BankAccount`.

        Examples:
            >>> data = {
                'account_number': 'foo',
                'bank_code': 'foo',
                'holder_name': 'foo',
                'routing_number': 'foo',
                'taxpayer_id' or 'ein': 'foo',
                'type': 'foo'
            }

        Args:
            data: dict of data

        Returns:
            response with instance of :class:`.BankAccount`
        """
        instance = Token.from_dict_or_instance(data)

        bank_account_type = instance.get_bank_account_type()
        if bank_account_type == BankAccount.INDIVIDUAL_TYPE:
            seller_response = self.search_individual_seller(  # type: ignore
                instance.taxpayer_id
            )
        elif bank_account_type == BankAccount.BUSINESS_TYPE:
            seller_response = self.search_business_seller(instance.ein)  # type: ignore
        else:
            raise TypeError("this is not supposed to happen!")

        seller_data = seller_response.data

        token_response = self.__add_bank_account_token(instance)
        created_token = token_response.data

        data = {"customer": seller_data["id"], "token": created_token["id"]}

        url = self._construct_url(action="bank_accounts")
        return self._post(url, data=data)

    def remove_bank_account(self, identifier: str):
        """
        Remove todas as :class:`.BankAccount` de um
        :class:`.Seller` usando o `identifier` deste.

        Args:
            identifier: uuid id

        Returns:
           :class:`.ZoopResponse`
        """
        url = self._construct_url(action="bank_accounts", identifier=identifier)
        return self._delete(url)
