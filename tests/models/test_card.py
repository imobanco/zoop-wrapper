from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.card import Card, CardVerificationChecklist
from tests.factories.card import CardFactory


class CardTestCase(SetTestCase):
    def test_get_required_fields(self):
        self.assertIsSubSet(
            {"expiration_month", "expiration_year", "holder_name"},
            Card.get_required_fields(),
        )

    def test_get_non_required_fields(self):
        self.assertIsSubSet(
            {
                "card_brand",
                "first4_digits",
                "last4_digits",
                "is_active",
                "is_valid",
                "is_verified",
                "fingerprint",
                "verification_checklist",
            },
            Card.get_non_required_fields(),
        )

    def test_init_custom_fields(self):
        instance = MagicMock()

        Card.init_custom_fields(instance)
        self.assertIsInstance(
            instance.verification_checklist, CardVerificationChecklist
        )

    def test_create(self):
        instance = CardFactory()
        self.assertIsInstance(instance, Card)
