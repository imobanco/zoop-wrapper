from unittest import TestCase

from ZoopAPIWrapper.models.bank_account import BankAccount, VerificationChecklist, Address


class BankAccountTestCase(TestCase):
    def test_from_dict(self):
        data = {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

            "holder_name": "foo",
            "taxpayer_id": "foo",
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
        instance = BankAccount.from_dict(data)

        self.assertIsInstance(instance, BankAccount)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.account_number, 'foo')
        self.assertEqual(instance.holder_name, 'foo')
        self.assertEqual(instance.bank_code, 'foo')
        self.assertEqual(instance.bank_name, 'foo')
        self.assertEqual(instance.routing_number, 'foo')
        self.assertEqual(instance.phone_number, 'foo')
        self.assertIsNone(instance.address)
        self.assertIsInstance(instance.verification_checklist, VerificationChecklist)
        self.assertEqual(instance.verification_checklist.deposit_check, 'foo')

    def test_to_dict(self):
        data = {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',
            "holder_name": "foo",
            "taxpayer_id": "foo",
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
        instance = BankAccount.from_dict(data)

        self.assertIsInstance(instance, BankAccount)
        self.assertEqual(instance.to_dict(), data)
