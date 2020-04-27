from .base import BaseZoopWrapper
from ..models.bank_account import BankAccount
from ..models.token import Token


class BankAccountWrapper(BaseZoopWrapper):
    """
    Possui os métodos do resource :class:`.BankAccount`

    .. warning:: Não importe isso diretamente!

        Essa classe precisa de métodos presentes em outro wrapper
    """

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
            seller_response = self.search_individual_seller(instance.taxpayer_id)  # type: ignore
        elif bank_account_type == BankAccount.BUSINESS_TYPE:
            seller_response = self.search_business_seller(instance.ein)  # type: ignore
        else:
            raise TypeError("this is not supposed to happen!")

        seller_instance = seller_response.instance

        token_response = self.__add_bank_account_token(instance)
        created_token = token_response.instance

        data = {"customer": seller_instance.id, "token": created_token.id}

        url = self._construct_url(action="bank_accounts")
        return self._post(url, data=data)
