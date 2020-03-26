from unittest import TestCase

from ZoopAPIWrapper.models.bank_account import VerificationChecklist
from ZoopAPIWrapper.models.factories.bank_account import (
    VerificationChecklistFactory)


class VerificationChecklistTestCase(TestCase):
    @property
    def data(self):
        return {
            "postal_code_check": 'foo',
            "address_line1_check": 'foo',
            "deposit_check": 'foo'
        }

    def test_create(self):
        instance = VerificationChecklistFactory()
        self.assertIsInstance(instance, VerificationChecklist)

    def test_from_dict(self):
        instance = VerificationChecklist.from_dict(self.data)

        self.assertIsInstance(instance, VerificationChecklist)
        self.assertEqual(instance.postal_code_check, 'foo')
        self.assertEqual(instance.address_line1_check, 'foo')
        self.assertEqual(instance.deposit_check, 'foo')

    def test_to_dict(self):
        instance = VerificationChecklist.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
