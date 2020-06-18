from typing import Union

from .base import BaseZoopWrapper
from ..models.transaction import Transaction


class TransactionWrapper(BaseZoopWrapper):
    """
    Possui os métodos do resource :class:`.Transaction`
    """

    def list_transactions(self):
        """
        list all transactions

        Returns:
            response
        """
        url = self._construct_url(action="transactions")
        return self._get(url)

    def list_transactions_for_seller(self, identifier):
        """
        list all transactions from seller

        Args:
            identifier: uuid id

        Returns:
            response
        """
        url = self._construct_url(
            action="sellers", identifier=identifier, subaction="transactions"
        )
        return self._get(url)

    def retrieve_transaction(self, identifier):
        """
        retrieve a transaction

        Args:
            identifier: uuid id

        Returns:
            response
        """
        url = self._construct_url(action="transactions", identifier=identifier)
        return self._get(url)

    def add_transaction(self, data: Union[dict, Transaction]):
        """
        add transaction

        Examples:
            data = {
                'amount' : 'foo',
                'currency' : 'BRL',
                'customer': 'foo',
                'description' : 'foo',
                'on_behalf_of' : 'foo',
                'payment_type' : 'foo',
                'reference_id' : 'foo',
                'payment_method' : {
                    'body_instructions' : instructions,
                    'expiration_date' : expiration_date,
                    'payment_limit_date' : payment_limit_date,
                    'billing_instructions' : {
                        'discount' : discount
                        'interest' : interest,
                        'late_fee' : late_fee,
                    }
                }
            }

            data = {
                'amount': '1000',
                'currency': 'BRL',
                'customer': 'buyer_id',
                'description': 'meu boleto gerado para teste',
                'on_behalf_of': 'seller_id',
                'payment_type': 'boleto',
                'payment_method': {
                    'expiration_date': '2020-06-20',
                    'payment_limit_date': '2020-06-30',
                    'billing_instructions': {
                        'late_fee': {
                            'mode': 'FIXED',
                            'percentage': 30,
                            'start_date': '2020-06-20'
                        },
                        'interest': {
                            'mode': 'MONTHLY_PERCENTAGE',
                            'percentage': 30,
                            'start_date': '2020-06-20'
                        },
                        'discount': [{
                            'amount': 300,
                            'limit_date': '2020-06-20'
                            'mode': 'FIXED',
                        }]
                    }
                }
            }

        Args:
            data: dict of data

        Returns:
            response with instance of Transaction
        """
        instance = Transaction.from_dict_or_instance(data)
        url = self._construct_url(action="transactions")
        return self._post_instance(url, instance=instance)

    def cancel_transaction(self, identifier):
        """
        cancel a transaction

        Args:
            identifier: uuid id

        Returns:
            response
        """
        transaction_response = self.retrieve_transaction(identifier)
        transaction = transaction_response.instance

        data = {
            "amount": transaction.amount,
            "on_behalf_of": transaction.on_behalf_of,
        }

        url = self._construct_url(
            action="transactions", identifier=identifier, subaction="void"
        )
        return self._post(url, data=data)
