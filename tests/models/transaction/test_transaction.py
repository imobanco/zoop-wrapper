from unittest.mock import MagicMock, patch

from tests.utils import SetTestCase
from zoop_wrapper.exceptions import ValidationError
from zoop_wrapper.models.transaction import Transaction, PointOfSale, History, Source
from zoop_wrapper.models.token import Token, Card
from zoop_wrapper.models.invoice import Invoice
from tests.factories.transaction import (
    TransactionFactory,
    TransactionCreditFactory,
    TransactionBoletoFactory,
)
from tests.factories.source import SourceCardPresentFactory, SourceCardNotPresentFactory


class TransactionTestCase(SetTestCase):
    def test_init_custom_fields_raise_type(self):
        instance = MagicMock()

        self.assertRaises(ValidationError, Transaction.init_custom_fields, instance)

    def test_init_custom_fields_created_invoice(self):
        instance = MagicMock()

        Transaction.init_custom_fields(
            instance, payment_type=Transaction.BOLETO_TYPE, id="foo", amount="23.45"
        )
        self.assertEqual(instance.amount, 2345)
        self.assertIsInstance(instance.payment_method, Invoice)
        self.assertIsInstance(instance.point_of_sale, PointOfSale)
        self.assertIsInstance(instance.history, list)
        self.assertEqual(len(instance.history), 1)
        self.assertIsInstance(instance.history[0], History)

    def test_init_custom_fields_created_card(self):
        instance = MagicMock()

        Transaction.init_custom_fields(
            instance, payment_type=Transaction.CARD_TYPE, id="foo", amount="23.45"
        )
        self.assertEqual(instance.amount, 2345)
        self.assertIsInstance(instance.payment_method, Card)
        self.assertIsInstance(instance.point_of_sale, PointOfSale)
        self.assertIsInstance(instance.history, list)
        self.assertEqual(len(instance.history), 1)
        self.assertIsInstance(instance.history[0], History)

    def test_init_custom_fields_created_raise(self):
        instance = MagicMock()

        self.assertRaises(
            ValidationError,
            Transaction.init_custom_fields,
            instance,
            amount="23.45",
            id="foo",
            payment_type="bar",
        )

    def test_init_custom_fields_created_float_parse(self):
        instance = MagicMock(amount=None)

        self.assertIsNone(instance.amount)

        Transaction.init_custom_fields(
            instance, payment_type=Transaction.BOLETO_TYPE, id="foo", amount="12.34"
        )

        self.assertEqual(instance.amount, 1234)

    def test_init_custom_fields_user_given_integer_amount(self):
        """
        Dado que um usuário criou a transação com amount 1234
        Quando init_custom_fields rodar
        Então o amount após conversão deve continuar sendo 1234
        """
        instance = MagicMock()

        Transaction.init_custom_fields(
            instance, payment_type=Transaction.BOLETO_TYPE, amount=1234
        )

        self.assertEqual(instance.amount, 1234)

    def test_init_custom_fields_user_given_float_amount(self):
        """
        Dado que um usuário criou a transação com amount 56.78
        Quando init_custom_fields rodar
        Então o amount após conversão deve ser 5678
        """
        instance = MagicMock()

        Transaction.init_custom_fields(
            instance, payment_type=Transaction.BOLETO_TYPE, amount=56.78
        )

        self.assertEqual(instance.amount, 5678)

    def test_init_custom_fields_invoice(self):
        instance = MagicMock()

        Transaction.init_custom_fields(
            instance, payment_type=Transaction.BOLETO_TYPE, amount=1234
        )
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
            amount=1234,
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
            amount=1234,
            allow_empty=True,
        )
        self.assertIsInstance(instance.source, Source)

    def test_non_required_fields(self):
        self.assertIsSubSet(
            {
                "app_transaction_uid",
                "business",
                "captured",
                "confirmed",
                "discounts",
                "expected_on",
                "fee_details",
                "fees",
                "gateway_authorizer",
                "history",
                "individual",
                "installment_plan",
                "location_latitude",
                "location_longitude",
                "original_amount",
                "point_of_sale",
                "pre_authorization",
                "reference_id",
                "refunded",
                "refunds",
                "rewards",
                "sales_receipt",
                "statement_descriptor",
                "status",
                "transaction_number",
                "voided",
            },
            Transaction.get_non_required_fields(),
        )

    def test_required_fields(self):
        self.assertEqual(
            {"currency", "customer", "description", "on_behalf_of", "payment_type",},
            Transaction.get_required_fields(),
        )

    def test_create(self):
        instance = TransactionBoletoFactory()
        self.assertIsInstance(instance, Transaction)

    def test_get_card_required_fields(self):
        self.assertEqual(
            {
                "currency",
                "customer",
                "description",
                "on_behalf_of",
                "payment_type",
                "source",
            },
            Transaction.get_card_required_fields(),
        )

    def test_get_boleto_required_fields(self):
        self.assertEqual(
            {
                "amount",
                "currency",
                "customer",
                "description",
                "on_behalf_of",
                "payment_method",
                "payment_type",
            },
            Transaction.get_boleto_required_fields(),
        )

    def test_get_validation_fields_credit(self):
        instance = TransactionCreditFactory()
        self.assertIsInstance(instance, Transaction)
        self.assertEqual(
            {
                "currency",
                "customer",
                "description",
                "on_behalf_of",
                "payment_type",
                "source",
            },
            instance.get_validation_fields(),
        )

    def test_get_validation_fields_boleto(self):
        instance = TransactionBoletoFactory()
        self.assertIsInstance(instance, Transaction)
        self.assertEqual(
            {
                "amount",
                "currency",
                "customer",
                "description",
                "on_behalf_of",
                "payment_method",
                "payment_type",
            },
            instance.get_validation_fields(),
        )

    def test_get_all_fields(self):
        with patch(
            "zoop_wrapper.models.transaction.Transaction.get_validation_fields"
        ) as mocked_get_validation_fields, patch(
            "zoop_wrapper.models.transaction.Transaction.get_non_required_fields"
        ) as mocked_get_non_required_fields:
            instance = TransactionBoletoFactory()

            mocked_get_validation_fields.reset_mock()
            mocked_get_non_required_fields.reset_mock()
            instance.get_all_fields()

            self.assertIsInstance(instance, Transaction)
            mocked_get_validation_fields.assert_called_once()
            mocked_get_non_required_fields.assert_called_once()
