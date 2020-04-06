from unittest.mock import MagicMock

from tests.utils import SetTestCase
from ZoopAPIWrapper.models.transaction import (
    Transaction, PointOfSale, History
)
from tests.factories.transaction import TransactionFactory
from ZoopAPIWrapper.models.invoice import Invoice


class TransactionTestCase(SetTestCase):
    # def test_init_custom_fields(self):
    #     instance = MagicMock()
    #
    #     Transaction.init_custom_fields(instance)
    #     self.assertIsInstance(instance.point_of_sale, PointOfSale)
    #     self.assertIsInstance(instance.history, list)
    #     self.assertEqual(len(instance.history), 1)
    #     self.assertIsInstance(instance.history[0], History)

    def test_init_custom_fields_invoice(self):
        instance = MagicMock()

        Transaction.init_custom_fields(
            instance, payment_type=Transaction.BOLETO_TYPE)
        self.assertIsInstance(instance.payment_method, Invoice)

    # def test_init_custom_fields_card(self):
    #     instance = MagicMock()
    #
    #     Transaction.init_custom_fields(
    #         instance, payment_type=Transaction.CREDIT_TYPE)
    #     self.assertIsInstance(instance.payment_method, dict)

    def test_non_required_fields(self):
        self.assertIsSubSet(
            {"status", "confirmed", "original_amount", "transaction_number",
             "gateway_authorizer", "app_transaction_uid", "refunds", "rewards",
             "discounts", "pre_authorization", "sales_receipt",
             "statement_descriptor", "point_of_sale", "installment_plan",
             "refunded", "voided", "captured", "fees", "fee_details",
             "location_latitude", "location_longitude", "individual",
             "business", "expected_on", "history"},
            Transaction.get_non_required_fields()
        )

    def test_required_fields(self):
        self.assertEqual(
            {'amount', 'currency', 'description', 'reference_id',
             'on_behalf_of', 'customer', 'payment_type', 'payment_method'},
            Transaction.get_required_fields()
        )

    def test_create(self):
        instance = TransactionFactory()
        self.assertIsInstance(instance, Transaction)
