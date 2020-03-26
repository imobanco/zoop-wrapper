from unittest import TestCase

from ZoopAPIWrapper.models.card import CardVerificationChecklist
from ZoopAPIWrapper.models.factories.card import (
    CardVerificationChecklistFactory
)


class CardVerificationChecklistTestCase(TestCase):
    @property
    def data(self):
        return {
            "postal_code_check": 'foo',
            "address_line1_check": 'foo',

            "security_code_check": 'foo'
        }

    def test_create(self):
        instance = CardVerificationChecklistFactory()
        self.assertIsInstance(instance, CardVerificationChecklist)

    def test_from_dict(self):
        instance = CardVerificationChecklist.from_dict(self.data)

        self.assertIsInstance(instance, CardVerificationChecklist)
        self.assertEqual(instance.postal_code_check, 'foo')
        self.assertEqual(instance.address_line1_check, 'foo')
        self.assertEqual(instance.security_code_check, 'foo')

    def test_to_dict(self):
        instance = CardVerificationChecklist.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
