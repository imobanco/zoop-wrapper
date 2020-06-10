from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.transaction import Source
from tests.factories.token import CreateCardTokenFactory
from tests.factories.source import SourceCardPresentFactory, SourceCardNotPresentFactory

from zoop_wrapper.models.token import Token
from zoop_wrapper.models.invoice import Invoice
from tests.factories.transaction import TransactionFactory

from zoop_wrapper.exceptions import ValidationError


class SourceTestCase(SetTestCase):
    def test_init_custom_fields_with_source_type_wrong(self):

        instance = MagicMock(SOURCE_TYPES={"foo"})

        self.assertRaises(
            ValidationError, Source.init_custom_fields, instance, type="bar"
        )

    def test_init_custom_fields_card_present_type(self):
        instance = MagicMock()

        Source.init_custom_fields(
            instance, card=CreateCardTokenFactory(), usage="single_use"
        )

        self.assertIsInstance(instance.card, Token)

    def test_required_fields(self):
        self.assertEqual(
            {"card", "type", "usage", "currency", "amount"},
            Source.get_required_fields(),
        )

    def test_create_card_present(self):
        instance = SourceCardPresentFactory()
        self.assertIsInstance(instance, Source)

    def test_create_card_not_present(self):
        instance = SourceCardNotPresentFactory(
            card=CreateCardTokenFactory(id="123"), usage="single_use", amount="567"
        )
        self.assertIsInstance(instance, Source)

    def test_get_card_not_present_required_fields(self):
        self.assertEqual(
            {"card", "type", "amount", "usage", "currency"},
            Source.get_card_not_present_required_fields(),
        )

    def test_get_card_present_required_fields(self):
        self.assertEqual(
            {"amount", "card", "currency", "type", "usage",},
            Source.get_card_present_required_fields(),
        )

    def test_get_validation_fields_card_not_present(self):
        instance = SourceCardNotPresentFactory(
            card=CreateCardTokenFactory(id="123"), usage="single_use", amount="500"
        )
        self.assertIsInstance(instance, Source)

        self.assertEqual(
            {"card", "type", "currency", "usage", "amount"},
            instance.get_validation_fields(),
        )

    def test_get_all_fields_card_not_present(self):
        instance = SourceCardNotPresentFactory(
            card=CreateCardTokenFactory(id="123"), usage="single_use", amount="500"
        )
        self.assertIsInstance(instance, Source)
        self.assertEqual(
            {"card", "currency", "type", "usage", "amount",}, instance.get_all_fields(),
        )

    def test_get_validation_fields_card_present(self):
        instance = SourceCardPresentFactory(card=CreateCardTokenFactory(id=None))
        self.assertIsInstance(instance, Source)

        self.assertEqual(
            {"card", "type", "usage", "currency", "amount",},
            instance.get_validation_fields(),
        )

    def test_get_all_fields_card_present(self):
        instance = SourceCardPresentFactory(card=CreateCardTokenFactory(id=None))
        self.assertIsInstance(instance, Source)
        self.assertEqual(
            {"card", "type", "usage", "currency", "amount",}, instance.get_all_fields(),
        )
