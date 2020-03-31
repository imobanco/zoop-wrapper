from tests.utils import MockedAddressLoggerTestCase as TestCase, SetTestCase
from ZoopAPIWrapper.models.base import Address
from ZoopAPIWrapper.models.bank_account import (
    BankAccount, BankAccountVerificationModel)
from ZoopAPIWrapper.models.factories.bank_account import (
    BankAccountFactory, IndividualBankAccountFactory,
    BusinessBankAccountFactory
)


class BankAccountTestCase(TestCase, SetTestCase):
    @property
    def data(self):
        return {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
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
            "address": {
                'state': 'foo',
                'country_code': 'foo',
                'postal_code': 'foo',
                'line2': 'foo',
                'neighborhood': 'foo',
                'city': 'foo',
                'line3': 'foo',
                'line1': 'foo'
            },
            "verification_checklist": {
                "postal_code_check": "foo",
                "address_line1_check": "foo",
                "deposit_check": "foo"
            }
        }

    def test_required_fields(self):
        self.assertIsSuperSet(
            {"holder_name", "description",
             "bank_name", "bank_code"},
            BankAccount.get_required_fields()
        )

    def test_non_required_fields(self):
        self.assertIsSubSet(
            {"type", "last4_digits", "account_number",
             "country_code", "routing_number", "phone_number",
             "is_active", "is_verified", "debitable", "customer",
             "fingerprint", "address", "verification_checklist"},
            BankAccount.get_non_required_fields()
        )

    def test_create(self):
        self.assertRaises(TypeError, BankAccountFactory)

    def test_create_individual(self):
        instance = IndividualBankAccountFactory()

        self.assertIsInstance(instance, BankAccount)

    def test_create_business(self):
        instance = BusinessBankAccountFactory()

        self.assertIsInstance(instance, BankAccount)

    def test_from_dict_individual(self):
        data = self.data
        data['taxpayer_id'] = 'foo'

        instance = BankAccount.from_dict(data)

        self.assertIsInstance(instance, BankAccount)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.account_number, 'foo')
        self.assertEqual(instance.holder_name, 'foo')
        self.assertEqual(instance.bank_code, 'foo')
        self.assertEqual(instance.taxpayer_id, 'foo')
        self.assertEqual(instance.routing_number, 'foo')
        self.assertEqual(instance.phone_number, 'foo')
        self.assertIsInstance(instance.address, Address)
        self.assertIsInstance(instance.verification_checklist,
                              BankAccountVerificationModel)
        self.assertEqual(instance.verification_checklist.deposit_check, 'foo')

    def test_from_dict_business(self):
        data = self.data
        data['ein'] = 'foo'

        instance = BankAccount.from_dict(data)

        self.assertIsInstance(instance, BankAccount)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.account_number, 'foo')
        self.assertEqual(instance.holder_name, 'foo')
        self.assertEqual(instance.bank_code, 'foo')
        self.assertEqual(instance.ein, 'foo')
        self.assertEqual(instance.routing_number, 'foo')
        self.assertEqual(instance.phone_number, 'foo')
        self.assertIsInstance(instance.address, Address)
        self.assertIsInstance(instance.verification_checklist,
                              BankAccountVerificationModel)
        self.assertEqual(instance.verification_checklist.deposit_check, 'foo')

    def test_to_dict(self):
        data = self.data
        data['taxpayer_id'] = 'foo'

        instance = BankAccount.from_dict(data)

        self.assertEqual(instance.to_dict(), data)
