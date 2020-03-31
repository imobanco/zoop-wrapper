from unittest import TestCase

from ZoopAPIWrapper.models.bank_account import BankAccountVerificationModel
from ZoopAPIWrapper.models.factories.bank_account import (
    BankAccountVerificationModelFactory
)


class BankAccountVerificationChecklistTestCase(TestCase):
    @property
    def data(self):
        return {
            "postal_code_check": 'foo',
            "address_line1_check": 'foo',

            "deposit_check": 'foo'
        }

    def test_create(self):
        instance = BankAccountVerificationModelFactory()
        self.assertIsInstance(instance, BankAccountVerificationModel)

    def test_from_dict(self):
        instance = BankAccountVerificationModel.from_dict(self.data)

        self.assertIsInstance(instance, BankAccountVerificationModel)
        self.assertEqual(instance.postal_code_check, 'foo')
        self.assertEqual(instance.address_line1_check, 'foo')
        self.assertEqual(instance.deposit_check, 'foo')

    def test_to_dict(self):
        instance = BankAccountVerificationModel.from_dict(self.data)

        self.assertIsInstance(instance, BankAccountVerificationModel)
