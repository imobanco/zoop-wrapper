from unittest import TestCase

from ZoopAPIWrapper.models.bank_account import VerificationChecklist


class VerificationChecklistTestCase(TestCase):
    def test_from_dict(self):
        data = {
            "postal_code_check": 'foo',
            "address_line1_check": 'foo',
            "deposit_check": 'foo'
        }
        instance = VerificationChecklist.from_dict(data)

        self.assertIsInstance(instance, VerificationChecklist)
        self.assertEqual(instance.postal_code_check, 'foo')
        self.assertEqual(instance.address_line1_check, 'foo')
        self.assertEqual(instance.deposit_check, 'foo')

    def test_to_dict(self):
        data = {
            "postal_code_check": 'foo',
            "address_line1_check": 'foo',
            "deposit_check": 'foo'
        }
        instance = VerificationChecklist.from_dict(data)

        self.assertIsInstance(instance, VerificationChecklist)
        self.assertEqual(instance.to_dict(), data)
