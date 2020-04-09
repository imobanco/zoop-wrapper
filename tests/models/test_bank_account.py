from unittest.mock import MagicMock

from tests.utils import MockedLoggerTestCase as TestCase, SetTestCase
from zoop_wrapper.models.base import Address
from zoop_wrapper.models.bank_account import BankAccount, BankAccountVerificationModel
from zoop_wrapper.exceptions import ValidationError
from tests.factories.bank_account import (
    BankAccountFactory,
    IndividualBankAccountFactory,
    BusinessBankAccountFactory,
)


class BankAccountTestCase(TestCase, SetTestCase):
    def test_required_fields(self):
        self.assertEqual(
            {"type", "holder_name", "bank_code", "routing_number"},
            BankAccount.get_required_fields(),
        )

    def test_non_required_fields(self):
        self.assertIsSubSet(
            {
                "bank_name",
                "account_number",
                "description",
                "last4_digits",
                "country_code",
                "phone_number",
                "is_active",
                "is_verified",
                "debitable",
                "customer",
                "fingerprint",
                "address",
                "verification_checklist",
            },
            BankAccount.get_non_required_fields(),
        )

    def test_create(self):
        self.assertRaises(ValidationError, BankAccountFactory)

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
        self.assertIsInstance(
            instance.verification_checklist, BankAccountVerificationModel
        )
