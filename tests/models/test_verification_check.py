from unittest import TestCase

from ZoopAPIWrapper.models.base import VerificationChecklist
from ZoopAPIWrapper.models.factories.base import (
    VerificationCheckListFactory)


class VerificationChecklistTestCase(TestCase):
    @property
    def data(self):
        return {
            "postal_code_check": 'foo',
            "address_line1_check": 'foo'
        }

    def test_create(self):
        instance = VerificationCheckListFactory()
        self.assertIsInstance(instance, VerificationChecklist)

    def test_from_dict(self):
        instance = VerificationChecklist.from_dict(self.data)

        self.assertIsInstance(instance, VerificationChecklist)
        self.assertEqual(instance.postal_code_check, 'foo')
        self.assertEqual(instance.address_line1_check, 'foo')

    def test_to_dict(self):
        instance = VerificationChecklist.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
