from unittest.mock import MagicMock, patch

from tests.utils import SetTestCase
from zoop_wrapper.models.transaction import Transaction, PointOfSale, History, Source
from zoop_wrapper.models.token import Token
from zoop_wrapper.models.invoice import Invoice
from tests.factories.transaction import (
    TransactionFactory,
    TransactionCredit,
    TransactionBoleto,
)
from tests.factories.source import SourceCardPresentFactory, SourceCardNotPresentFactory


class TransactionTestCase(SetTestCase):
    def test_init_custom_fields_raise_type(self):
        instance = MagicMock()

        self.assertRaises(ValueError, Transaction.init_custom_fields, instance)

    def test_init_custom_fields_invoice(self):
        instance = MagicMock()

        Transaction.init_custom_fields(instance, payment_type=Transaction.BOLETO_TYPE)
        self.assertIsInstance(instance.payment_method, Invoice)
        self.assertIsInstance(instance.point_of_sale, PointOfSale)
        self.assertIsInstance(instance.history, list)
        self.assertEqual(len(instance.history), 1)
        self.assertIsInstance(instance.history[0], History)

    def test_init_custom_fields_source_card_present(self):
        instance = MagicMock()

        Transaction.init_custom_fields(
            instance,
            payment_type=Transaction.CARD_TYPE,
            source=SourceCardPresentFactory().to_dict(),
        )
        self.assertIsInstance(instance.source, Source)

    def test_init_custom_fields_source_card_not_present(self):
        instance = MagicMock()

        Transaction.init_custom_fields(
            instance,
            payment_type=Transaction.CARD_TYPE,
            source=SourceCardNotPresentFactory(
                amount=1234, usage="single_use"
            ).to_dict(),
            allow_empty=True,
        )
        self.assertIsInstance(instance.source, Source)

    def test_non_required_fields(self):
        self.assertIsSubSet(
            {
                "status",
                "confirmed",
                "original_amount",
                "transaction_number",
                "gateway_authorizer",
                "app_transaction_uid",
                "refunds",
                "rewards",
                "discounts",
                "pre_authorization",
                "sales_receipt",
                "statement_descriptor",
                "point_of_sale",
                "installment_plan",
                "refunded",
                "voided",
                "captured",
                "fees",
                "fee_details",
                "location_latitude",
                "location_longitude",
                "individual",
                "business",
                "expected_on",
                "history",
                "reference_id",
            },
            Transaction.get_non_required_fields(),
        )

    def test_required_fields(self):
        self.assertEqual(
            {
                "amount",
                "currency",
                "description",
                "on_behalf_of",
                "customer",
                "payment_type",
            },
            Transaction.get_required_fields(),
        )

    def test_create(self):
        instance = TransactionBoleto()
        self.assertIsInstance(instance, Transaction)

    def test_get_card_required_fields(self):
        self.assertEqual(
            {
                "source",
                "description",
                "amount",
                "currency",
                "payment_type",
                "on_behalf_of",
                "customer",
            },
            Transaction.get_card_required_fields(),
        )

    def test_get_boleto_required_fields(self):
        self.assertEqual(
            {
                "payment_method",
                "customer",
                "payment_type",
                "amount",
                "description",
                "currency",
                "on_behalf_of",
            },
            Transaction.get_boleto_required_fields(),
        )

    def test_get_validation_fields_credit(self):
        instance = TransactionCredit()
        self.assertIsInstance(instance, Transaction)
        self.assertEqual(
            {
                "customer",
                "payment_type",
                "description",
                "on_behalf_of",
                "currency",
                "amount",
                "source",
            },
            instance.get_validation_fields(),
        )

    def test_get_validation_fields_boleto(self):
        instance = TransactionBoleto()
        self.assertIsInstance(instance, Transaction)
        self.assertEqual(
            {
                "payment_method",
                "on_behalf_of",
                "currency",
                "payment_type",
                "amount",
                "customer",
                "description",
            },
            instance.get_validation_fields(),
        )

    def test_get_all_fields(self):
        with patch(
            "zoop_wrapper.models.transaction.Transaction.get_validation_fields"
        ) as mocked_get_validation_fields, patch(
            "zoop_wrapper.models.transaction.Transaction.get_non_required_fields"
        ) as mocked_get_non_required_fields:
            instance = TransactionBoleto()

            mocked_get_validation_fields.reset_mock()
            mocked_get_non_required_fields.reset_mock()
            instance.get_all_fields()

            self.assertIsInstance(instance, Transaction)
            mocked_get_validation_fields.assert_called_once()
            mocked_get_non_required_fields.assert_called_once()
