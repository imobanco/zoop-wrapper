from unittest.mock import patch

from tests.utils import APITestCase
from zoop_wrapper.models.transaction import Transaction, Source
from zoop_wrapper.models.base import PaymentMethod
from tests.factories.transaction import (
    CancelTransactionCardFactory,
    TransactionBoletoFactory,
    TransactionCreditFactory,
    TransactionFactory,
)
from zoop_wrapper.models.card import Card
from zoop_wrapper.models.invoice import Invoice
from zoop_wrapper.models.token import Token


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
                    "late_fee": {
                        "mode": "FIXED",
                        "percentage": 30,
                        "start_date": "2020-06-20",
                    },
                    "interest": {
                        "mode": "MONTHLY_PERCENTAGE",
                        "percentage": 30,
                        "start_date": "2020-06-20",
                    },
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
            },
        }

        response = self.client.add_transaction(data)
        self.assertEqual(response.status_code, 201, msg=response.data)
        self.assertEqual(response.instance.payment_type, "credit")
        self.assertIsInstance(response.instance.source.card, Token)
        self.assertIsInstance(response.instance.source, Source)

    def test_cancel_transaction(self):
        self.set_post_mock(200, CancelTransactionCardFactory(id="foo").to_dict())

        with patch(
            "zoop_wrapper.wrapper.transaction.TransactionWrapper.retrieve_transaction"
        ) as mocked_retrieve_transaction:

            response = self.client.cancel_transaction("foo")
            self.assertEqual(response.status_code, 200, msg=response.data)
            mocked_retrieve_transaction.assert_called_once()
