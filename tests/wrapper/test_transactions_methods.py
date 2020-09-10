from unittest.mock import patch

from tests.utils import APITestCase
from zoop_wrapper.models.transaction import Transaction, Source
from zoop_wrapper.models.base import PaymentMethod
from tests.factories.transaction import (
    CancelTransactionCardFactory,
    TransactionBoletoFactory,
    TransactionCreditFactory,
)
from zoop_wrapper.models.token import Token
from zoop_wrapper.exceptions import ValidationError


class TransactionWrapperMethodsTestCase(APITestCase):
    def test_list_transactions(self):
        """
        Test list_transactions method
        """
        self.set_get_mock(200, {"items": [TransactionBoletoFactory()]})

        response = self.client.list_transactions()
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get("items")
        self.assertTrue(items)

    def test_list_transactions_for_seller(self):
        """
        Test list_transactions_for_seller method
        """
        self.set_get_mock(
            200, {"items": [TransactionBoletoFactory(on_behalf_of="foo")]}
        )

        response = self.client.list_transactions_for_seller("foo")
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get("items")
        self.assertTrue(items)

    def test_retrieve_transaction(self):
        """
        Test retrieve_transaction method.
        """
        self.set_get_mock(200, TransactionBoletoFactory(id="foo").to_dict())

        response = self.client.retrieve_transaction("foo")
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get("id"), "foo")
        self.assertIsInstance(response.instance, Transaction)
        self.assertEqual(response.instance.id, "foo")

    def test_add_transaction_invoice(self):
        self.set_post_mock(201, TransactionBoletoFactory().to_dict())

        data = {
            "amount": "1000",
            "currency": "BRL",
            "customer": "buyer_id",
            "description": "meu boleto gerado para teste",
            "on_behalf_of": "seller_id",
            "payment_type": "boleto",
            "payment_method": {
                "expiration_date": "2020-06-20",
                "payment_limit_date": "2020-06-30",
                "billing_instructions": {
                    "late_fee": {"mode": "FIXED", "amount": 300,},
                    "interest": {"mode": "MONTHLY_PERCENTAGE", "percentage": 2,},
                    "discount": [
                        {"mode": "FIXED", "amount": 300, "limit_date": "2020-06-20"}
                    ],
                },
            },
        }

        response = self.client.add_transaction(data)
        self.assertEqual(response.status_code, 201, msg=response.data)
        self.assertEqual(response.instance.payment_type, "boleto")
        self.assertIsInstance(response.instance.payment_method, PaymentMethod)

    def test_add_transaction_card_present(self):
        self.set_post_mock(201, TransactionCreditFactory().to_dict())

        data = {
            "amount": -5658.2277,
            "customer": "daef3fbc-a95a-4e18-9515-2e6915f639ad",
            "description": "Per hold relationship message suffer economy.",
            "on_behalf_of": "94ea79f2-6fc0-4551-b409-824f140f6a2e",
            "original_amount": -1776.0,
            "payment_type": "credit",
            "capture": True,
            "reference_id": "Exactly there develop.",
            "source": {
                "card": {
                    "card_number": "3539736185431858",
                    "expiration_month": 2,
                    "expiration_year": 2011,
                    "holder_name": "Michael Baker",
                    "security_code": "912",
                },
                "amount": -5658.2277,
                "currency": "BRL",
                "type": "card",
                "usage": "single_use",
                "installment_plan": {"mode": "interest_free", "number_installments": 5},
            },
        }

        response = self.client.add_transaction(data)
        self.assertEqual(response.status_code, 201, msg=response.data)
        self.assertEqual(response.instance.payment_type, "credit")
        self.assertIsInstance(response.instance.source.card, Token)
        self.assertIsInstance(response.instance.source, Source)

    def test_add_transaction_card_not_present(self):
        self.set_post_mock(201, TransactionCreditFactory().to_dict())

        data = {
            "amount": -5658.2277,
            "currency": "BRL",
            "customer": "daef3fbc-a95a-4e18-9515-2e6915f639ad",
            "description": "Per hold relationship message suffer economy.",
            "on_behalf_of": "94ea79f2-6fc0-4551-b409-824f140f6a2e",
            "original_amount": -1776.0,
            "payment_type": "credit",
            "capture": True,
            "reference_id": "Exactly there develop.",
            "source": {
                "amount": 1234,
                "card": {"id": "5000be1e-3e68-4296-9780-a39b1fcd08f1"},
                "type": "card",
                "usage": "single_use",
                "installment_plan": {
                    "mode": "interest_free",
                    "number_installments": 5,
                },
            },
        }

        response = self.client.add_transaction(data)
        self.assertEqual(response.status_code, 201, msg=response.data)
        self.assertEqual(response.instance.payment_type, "credit")
        self.assertIsInstance(response.instance.source.card, Token)
        self.assertIsInstance(response.instance.source, Source)

    def test__capture_or_void_transaction(self):
        """
        Dado que existe transação t1
        Quando for chamado ZoopWrapper().__capture_or_void_transaction(t1.id, 'void')
        Então:
            - TransactionWrapper.retrieve_transaction deve ter sido chamado
            - deve ter sido feito um post corretamente
        """
        self.set_post_mock(200, CancelTransactionCardFactory(id="foo").to_dict())

        with patch(
            "zoop_wrapper.wrapper.transaction.TransactionWrapper.retrieve_transaction"
        ) as mocked_retrieve_transaction:

            t1 = TransactionCreditFactory(id="1", allow_empty=True)

            mocked_retrieve_transaction.return_value = self.build_response_mock(
                200, instance=t1
            )

            response = self.client._capture_or_void_transaction(t1.id, "void")
            self.assertEqual(response.status_code, 200, msg=response.data)
            mocked_retrieve_transaction.assert_called_once()

            expected_data = {"amount": t1.amount, "on_behalf_of": t1.on_behalf_of}

            self.mocked_post.assert_called_once_with(
                f"{self.base_url}/transactions/{t1.id}/void/",
                json=expected_data,
                auth=self.auth,
            )

    def test__capture_or_void_transaction_amount(self):
        """
        Dado que existe transação t1 de 10000
        Quando for chamado ZoopWrapper().__capture_or_void_transaction(t1.id, 'void', 100.00)  # noqa
        Então:
            - TransactionWrapper.retrieve_transaction deve ter sido chamado
            - deve ter sido feito um post corretamente
        """
        self.set_post_mock(200, CancelTransactionCardFactory(id="foo").to_dict())

        with patch(
            "zoop_wrapper.wrapper.transaction.TransactionWrapper.retrieve_transaction"
        ) as mocked_retrieve_transaction:

            t1 = TransactionCreditFactory(id="1", amount=10000, allow_empty=True)

            mocked_retrieve_transaction.return_value = self.build_response_mock(
                200, instance=t1
            )

            response = self.client._capture_or_void_transaction(t1.id, "void", 100.00)
            self.assertEqual(response.status_code, 200, msg=response.data)
            mocked_retrieve_transaction.assert_called_once()

            expected_data = {"amount": 10000, "on_behalf_of": t1.on_behalf_of}

            self.mocked_post.assert_called_once_with(
                f"{self.base_url}/transactions/{t1.id}/void/",
                json=expected_data,
                auth=self.auth,
            )

    def test__capture_or_void_transaction_amount_invalid(self):
        """
        Dado que existe transação t1 de 10000
        Quando for chamado ZoopWrapper().__capture_or_void_transaction(t1.id, 'void', 100.01)  # noqa
        Então:
            - TransactionWrapper.retrieve_transaction deve ter sido chamado
            - não deve ter sido feito um post
            - deve ter sido levantado um ValidationError com o texto correto
        """
        self.set_post_mock(200, CancelTransactionCardFactory(id="foo").to_dict())

        with patch(
            "zoop_wrapper.wrapper.transaction.TransactionWrapper.retrieve_transaction"
        ) as mocked_retrieve_transaction:

            t1 = TransactionCreditFactory(id="1", amount=10000, allow_empty=True)

            mocked_retrieve_transaction.return_value = self.build_response_mock(
                200, instance=t1
            )

            with self.assertRaises(ValidationError) as error_context:
                self.client._capture_or_void_transaction(t1.id, "void", 100.01)

            self.assertIn(
                "A quantia 10001 é maior", str(error_context.exception.errors[0])
            )

            mocked_retrieve_transaction.assert_called_once()

            self.mocked_post.assert_not_called()

    def test__capture_or_void_transaction_sub_action_invalid(self):
        """
        Dado que existe transação t1 de 10000
        Quando for chamado ZoopWrapper().__capture_or_void_transaction('1', 'foo')
        Então:
            - TransactionWrapper.retrieve_transaction deve ter sido chamado
            - não deve ter sido feito um post
            - deve ter sido levantado um ValidationError com o texto correto
        """

        with patch(
            "zoop_wrapper.wrapper.transaction.TransactionWrapper.retrieve_transaction"
        ) as mocked_retrieve_transaction:

            with self.assertRaises(ValidationError) as error_context:
                self.client._capture_or_void_transaction("1", "foo")

            self.assertIn(
                "Deveria ser um dos valores", str(error_context.exception.errors[0])
            )

            mocked_retrieve_transaction.assert_not_called()

            self.mocked_post.assert_not_called()

    def test_cancel_transaction(self):
        """
        Dado N/A
        Quando for chamado ZoopWrapper().cancel_transaction('foo', 10)
        Então ZoopWrapper().__capture_or_void_transaction('foo', 'void', 10) deve ter sido chamado  # noqa
        """
        with patch(
            "zoop_wrapper.wrapper.transaction."
            "TransactionWrapper._capture_or_void_transaction"
        ) as mocked_method:
            self.client.cancel_transaction("foo", 10)

            mocked_method.assert_called_once_with("foo", "void", 10)

    def test_capture_transaction(self):
        """
        Dado N/A
        Quando for chamado ZoopWrapper().capture_transaction('foo', 10)
        Então ZoopWrapper().__capture_or_void_transaction('foo', 'capture', 10) deve ter sido chamado  # noqa
        """
        with patch(
            "zoop_wrapper.wrapper.transaction."
            "TransactionWrapper._capture_or_void_transaction"
        ) as mocked_method:
            self.client.capture_transaction("foo", 10)

            mocked_method.assert_called_once_with("foo", "capture", 10)
