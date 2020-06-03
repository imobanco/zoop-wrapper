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

        Source.init_custom_fields(instance, source_type="card_present_type",
                                  card=CardFactory())
        self.assertIsInstance(instance.card, Card)

    def test_init_custom_fields_card_present_not_type(self):
        instance = MagicMock()

        Source.init_custom_fields(instance, source_type="card_not_present_type",
                                  card=CardFactory(id="1"))
        self.assertIsInstance(instance.card, Card)

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
    def test_non_required_fields(self):
        self.assertIsSubSet(
            {
                "amount",
                "currency",
                "usage",
            },
            Source.get_non_required_fields(),
        )

    def test_required_fields(self):
        self.assertEqual(
            {
                "card",
                "type",
            },
            Source.get_required_fields(),
        )

    # def test_create(self):
    #     instance = SourceFactory()
    #     self.assertIsInstance(instance, Source)
