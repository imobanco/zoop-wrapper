from tests.utils import APITestCase
from zoop_wrapper.models.transaction import Transaction, Source
from tests.factories.transaction import (
    TransactionFactory,
    TransactionCredit,
    TransactionBoleto,
)
from zoop_wrapper.models.card import Card
from zoop_wrapper.models.invoice import Invoice
from zoop_wrapper.models.token import Token


class TransactionWrapperMethodsTestCase(APITestCase):
    def test_list_transactions(self):
        """
        Test list_transactions method
        """
        self.set_get_mock(200, {"items": [TransactionFactory()]})

        response = self.client.list_transactions()
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get("items")
        self.assertTrue(items)

    def test_list_transactions_for_seller(self):
        """
        Test list_transactions_for_seller method
        """
        self.set_get_mock(200, {"items": [TransactionFactory(on_behalf_of="foo")]})

        response = self.client.list_transactions_for_seller("foo")
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get("items")
        self.assertTrue(items)

    def test_retrieve_transaction(self):
        """
        Test retrieve_transaction method.
        """
        self.set_get_mock(200, TransactionFactory(id="foo").to_dict())

        response = self.client.retrieve_transaction("foo")
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get("id"), "foo")
        self.assertIsInstance(response.instance, Transaction)
        self.assertEqual(response.instance.id, "foo")

    def test_add_transaction(self):
        self.set_post_mock(201, TransactionFactory().to_dict())

        data = {
            "amount": "1000",
            "currency": "BRL",
            "description": "meu boleto gerado para teste",
            "on_behalf_of": "seller_id",
            "customer": "buyer_id",
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

    def test_add_transaction_credit(self):
        self.set_post_mock(201, TransactionCredit().to_dict())

        # print(TransactionCredit().to_dict())

        data = {
            "original_amount": -1776.0,
            "point_of_sale": {"entry_mode": "barcode", "identification_number": 123},
            "expected_on": "2020-6-4",
            "resource": "transaction",
            "source": {
                "card": {
                    "expiration_month": 2,
                    "created_at": "1933-03-06",
                    "used": True,
                    "id": "5000be1e-3e68-4296-9780-a39b1fcd08f1",
                    "updated_at": "2020-06-01",
                    "holder_name": "Michael Baker",
                    "security_code": "912",
                    "resource": "token",
                    "uri": "https://willis.biz/explore/explore/author/",
                    "card_number": "3539736185431858",
                    "expiration_year": 2011,
                },
                "type": "card",
            },
            "statement_descriptor": "Could.",
            "created_at": "1908-09-09",
            "customer": "daef3fbc-a95a-4e18-9515-2e6915f639ad",
            "id": "e45d8840-a5f6-4536-bc6f-898a072a9ec0",
            "captured": False,
            "uri": "https://www.peterson.net/terms.jsp",
            "currency": "BRL",
            "reference_id": "Exactly there develop.",
            "history": [
                {
                    "status": "succeeded",
                    "transaction": "1e2c6fc1-ec9f-4ca5-ad96-218907543062",
                    "id": "73119f1e-b56b-4057-848f-b10db0dd6759",
                    "created_at": "2018-12-24",
                    "amount": 5.35,
                    "operation_type": "created",
                }
            ],
            "payment_type": "credit",
            "on_behalf_of": "94ea79f2-6fc0-4551-b409-824f140f6a2e",
            "status": "failed",
            "confirmed": "0",
            "fees": "0.0",
            "voided": True,
            "refunded": False,
            "updated_at": "2020-06-01",
            "amount": -5658.2277,
            "payment_method": {
                "downloaded": True,
                "bank_code": 275,
                "url": "http://taylor-abbott.com/blog/list/categories/terms.html",
                "sequence": 732,
                "zoop_boleto_id": "f656d59b-3c77-470b-9dbc-3edd7d8516fe",
                "fingerprint": "9bf84367-f56f-41d0-9110-c44767444e27",
                "status": "not_paid",
                "paid_at": "2020-06-01",
                "reference_number": 5032,
                "body_instructions": ["pague este boleto!"],
                "document_number": 97,
                "recipient": "Rich, Kemp and Serrano",
                "accepted": False,
                "printed": False,
                "payment_limit_date": "2020-06-4",
                "barcode": 6616,
                "billing_instructions": {
                    "interest": {
                        "start_date": "2020-06-02",
                        "mode": "PERCENTAGE",
                        "percentage": -2056.6,
                    },
                    "late_fee": {
                        "start_date": "2020-06-02",
                        "mode": "FIXED",
                        "amount": -2717.214,
                    },
                    "discount": [
                        {"limit_date": "2020-06-02", "mode": "FIXED", "amount": -623.0,}
                    ],
                },
                "expiration_date": "2020-06-03",
            },
            "description": "Per hold relationship message suffer economy.",
        }

        response = self.client.add_transaction(data)
        self.assertEqual(response.status_code, 201, msg=response.data)
        self.assertEqual(response.instance.payment_type, "credit")
        self.assertIsInstance(response.instance.source.card, Token)
        self.assertIsInstance(response.instance.source, Source)

    # def test_cancel_transaction(self):
    # @TODO: terminar cancel transaction
    #
    #     self.set_delete_mock(
    #         200,
    #         {
    #             'id': 'foo',
    #             'resource': 'buyer',
    #             'deleted': True
    #         }
    #     )
    #
    #     response = self.client.remove_buyer('foo')
    #     self.assertEqual(response.status_code, 200, msg=response.data)
