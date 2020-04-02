from unittest.mock import MagicMock

from tests.utils import SetTestCase
from ZoopAPIWrapper.models.card import CardVerificationChecklist
from ZoopAPIWrapper.models.factories.card import (
    CardVerificationChecklistFactory
)


class CardVerificationChecklistTestCase(SetTestCase):
    def test_get_required_fields(self):
        self.assertIsSubSet(
            {'security_code_check'},
            CardVerificationChecklist.get_required_fields()
        )

    def test_create(self):
        instance = CardVerificationChecklistFactory()
        self.assertIsInstance(instance, CardVerificationChecklist)
