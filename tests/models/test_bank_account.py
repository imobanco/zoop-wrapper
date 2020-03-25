from unittest import TestCase

from ZoopAPIWrapper.models.bank_account import (
    BankAccount, IndividualBankAccount,
    BusinessBankAccount, VerificationChecklist)


class BankAccountTestCase(TestCase):
    @property
    def data(self):
        return {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

            "holder_name": "foo",
            "description": "foo",
            "bank_name": "foo",
            "bank_code": "foo",
            "type": "foo",
            "last4_digits": "foo",
            "account_number": "foo",
            "country_code": "foo",
            "routing_number": "foo",
            "phone_number": 'foo',
            "is_active": 'foo',
            "is_verified": 'foo',
            "debitable": 'foo',
            "customer": "foo",
            "fingerprint": "foo",
            "address": None,
            "verification_checklist": {
                "postal_code_check": "foo",
                "address_line1_check": "foo",
                "deposit_check": "foo"
            }
        }

    def test_from_dict_individual(self):
        data = self.data
        data['taxpayer_id'] = 'foo'

        instance = BankAccount.from_dict(data)

        self.assertIsInstance(instance, IndividualBankAccount)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.account_number, 'foo')
        self.assertEqual(instance.holder_name, 'foo')
        self.assertEqual(instance.bank_code, 'foo')
        self.assertEqual(instance.taxpayer_id, 'foo')
        self.assertEqual(instance.routing_number, 'foo')
        self.assertEqual(instance.phone_number, 'foo')
        self.assertIsNone(instance.address)
        self.assertIsInstance(instance.verification_checklist,
                              VerificationChecklist)
        self.assertEqual(instance.verification_checklist.deposit_check, 'foo')

    def test_from_dict_business(self):
        data = self.data
        data['ein'] = 'foo'

        instance = BankAccount.from_dict(data)

        self.assertIsInstance(instance, BusinessBankAccount)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.account_number, 'foo')
        self.assertEqual(instance.holder_name, 'foo')
        self.assertEqual(instance.bank_code, 'foo')
        self.assertEqual(instance.ein, 'foo')
        self.assertEqual(instance.routing_number, 'foo')
        self.assertEqual(instance.phone_number, 'foo')
        self.assertIsNone(instance.address)
        self.assertIsInstance(instance.verification_checklist,
                              VerificationChecklist)
        self.assertEqual(instance.verification_checklist.deposit_check, 'foo')

    def test_to_dict(self):
        data = self.data
        data['taxpayer_id'] = 'foo'

        instance = BankAccount.from_dict(data)

        """We remove the address because it's value is none.
        So it won't return on to_dict method"""
        data.pop('address')

        self.assertEqual(instance.to_dict(), data)
