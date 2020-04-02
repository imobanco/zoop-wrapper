from unittest.mock import MagicMock

from tests.utils import MockedAddressLoggerTestCase as TestCase, SetTestCase
from ZoopAPIWrapper.models.base import Address
from ZoopAPIWrapper.models.bank_account import (
    BankAccount, BankAccountVerificationModel)
from tests.factories.bank_account import (
    BankAccountFactory, IndividualBankAccountFactory,
    BusinessBankAccountFactory
)


class BankAccountTestCase(TestCase, SetTestCase):
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

    def test_init_custom_fields_business(self):
        instance = MagicMock()

        BankAccount.init_custom_fields(instance)
        self.assertIsInstance(instance.address, Address)
        self.assertIsInstance(instance.verification_checklist,
                              BankAccountVerificationModel)
