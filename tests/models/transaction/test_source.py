from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.transaction import Source
from tests.factories.card import CardFactory
from tests.factories.source import SourceCardPresentFactory, SourceCardNotPresentFactory

from zoop_wrapper.models.card import Card
from zoop_wrapper.models.invoice import Invoice
from tests.factories.transaction import TransactionFactory


class SourceTestCase(SetTestCase):
    def test_init_custom_fields_raise_type(self):
        instance = MagicMock()

        self.assertRaises(ValueError, Source.init_custom_fields, instance)

    def test_init_custom_fields_card_present_type(self):
        instance = MagicMock()

        Source.init_custom_fields(instance, card=CardFactory(), usage="single_use")

        self.assertIsInstance(instance.card, Card)

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

    def test_create_card_present(self):
        instance = SourceCardPresentFactory()
        self.assertIsInstance(instance, Source)

    def test_create_card_not_present(self):
        instance = SourceCardNotPresentFactory(card=CardFactory(id="123"))
        self.assertIsInstance(instance, Source)

    def test_get_card_not_present_required_fields(self):
        self.assertEqual(
            {
                "card",
                "type",
            },
            Source.get_card_not_present_required_fields(),
        )

    def test_get_card_present_required_fields(self):
        self.assertEqual(
            {
                "amount",
                "card",
                "currency",
                "type",
                "usage",
            },
            Source.get_card_present_required_fields(),
        )

    def test_get_validation_fields_card_not_present(self):
        instance = SourceCardNotPresentFactory(card=CardFactory(id="123"))
        self.assertIsInstance(instance, Source)

        self.assertEqual(
            {
                "card",
                "type",
            },
            instance.get_validation_fields(),
        )

    def test_get_all_fields_card_not_present(self):
        instance = SourceCardNotPresentFactory(card=CardFactory(id="123"))
        self.assertIsInstance(instance, Source)
        self.assertEqual(
            {
                "card",
                "type",
            },
            instance.get_all_fields(),
        )

    def test_get_validation_fields_card_present(self):
        instance = SourceCardPresentFactory()
        self.assertIsInstance(instance, Source)

        self.assertEqual(
            {
                "card",
                "type",
                "usage",
                "currency",
                "amount",

            },
            instance.get_validation_fields(),
        )

    def test_get_all_fields_card_present(self):
        instance = SourceCardPresentFactory()
        self.assertIsInstance(instance, Source)
        self.assertEqual(
            {
                "card",
                "type",
                "usage",
                "currency",
                "amount",
            },
            instance.get_all_fields(),
        )