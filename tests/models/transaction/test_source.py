from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.transaction import Source
from tests.factories.card import CardFactory
from zoop_wrapper.models.card import Card
from zoop_wrapper.models.invoice import Invoice
from tests.factories.transaction import TransactionFactory


class SourceTestCase(SetTestCase):
    def test_init_custom_fields_raise_type(self):
        instance = MagicMock()

        self.assertRaises(ValueError, Source.init_custom_fields, instance)

    def test_init_custom_fields_card_present_type(self):
        instance = MagicMock()

        Source.init_custom_fields(instance, source_type="card_present_type", card=CardFactory())
        # self.assertIsInstance(instance.payment_method, Invoice)
        # self.assertIsInstance(instance.point_of_sale, PointOfSale)
        # self.assertIsInstance(instance.history, list)
        # self.assertEqual(len(instance.history), 1)
        # self.assertIsInstance(instance.history[0], History)

    def test_init_custom_fields_card_present_not_type(self):
        instance = MagicMock()

        Source.init_custom_fields(instance, source_type="card_not_present_type", card=CardFactory(id="1"))
        # self.assertIsInstance(instance.payment_method, Invoice)
        # self.assertIsInstance(instance.point_of_sale, PointOfSale)
        # self.assertIsInstance(instance.history, list)
        # self.assertEqual(len(instance.history), 1)
        # self.assertIsInstance(instance.history[0], History)

    # def test_init_custom_fields_card(self):
    #     instance = MagicMock()
    #
    #     Transaction.init_custom_fields(instance, payment_type=Transaction.CREDIT_TYPE)
    #     self.assertIsInstance(instance.payment_method, Card)
    #     self.assertIsInstance(instance.point_of_sale, PointOfSale)
    #     self.assertIsInstance(instance.history, list)
    #     self.assertEqual(len(instance.history), 1)
    #     self.assertIsInstance(instance.history[0], History)
    #
    # def test_non_required_fields(self):
    #     self.assertIsSubSet(
    #         {
    #             "status",
    #             "confirmed",
    #             "original_amount",
    #             "transaction_number",
    #             "gateway_authorizer",
    #             "app_transaction_uid",
    #             "refunds",
    #             "rewards",
    #             "discounts",
    #             "pre_authorization",
    #             "sales_receipt",
    #             "statement_descriptor",
    #             "point_of_sale",
    #             "installment_plan",
    #             "refunded",
    #             "voided",
    #             "captured",
    #             "fees",
    #             "fee_details",
    #             "location_latitude",
    #             "location_longitude",
    #             "individual",
    #             "business",
    #             "expected_on",
    #             "history",
    #             "reference_id",
    #         },
    #         Transaction.get_non_required_fields(),
    #     )
    #
    # def test_required_fields(self):
    #     self.assertEqual(
    #         {
    #             "amount",
    #             "currency",
    #             "description",
    #             "on_behalf_of",
    #             "customer",
    #             "payment_type",
    #             "payment_method",
    #         },
    #         Transaction.get_required_fields(),
    #     )
    #
    # def test_create(self):
    #     instance = TransactionFactory()
    #     self.assertIsInstance(instance, Transaction)
