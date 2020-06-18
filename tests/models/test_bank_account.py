from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.base import Address
from zoop_wrapper.models.bank_account import BankAccount, BankAccountVerificationModel
from zoop_wrapper.exceptions import ValidationError
from tests.factories.bank_account import (
    BankAccountFactory,
    IndividualBankAccountFactory,
    BusinessBankAccountFactory,
)


class BankAccountTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertEqual(
            {"type", "holder_name", "bank_code", "routing_number"},
            BankAccount.get_required_fields(),
        )

    def test_non_required_fields(self):
        self.assertIsSubSet(
            {
                "account_number",
                "address",
                "bank_name",
                "country_code",
                "customer",
                "debitable",
                "description",
                "fingerprint",
                "is_active",
                "is_verified",
                "last4_digits",
                "phone_number",
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
