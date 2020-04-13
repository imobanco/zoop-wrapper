from tests.utils import SetTestCase
from zoop_wrapper.models.bank_account import BankAccountVerificationModel
from tests.factories.bank_account import BankAccountVerificationModelFactory


class BankAccountVerificationChecklistTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertIsSubSet(
            {"deposit_check"}, BankAccountVerificationModel.get_required_fields()
        )

    def test_create(self):
        instance = BankAccountVerificationModelFactory()
        self.assertIsInstance(instance, BankAccountVerificationModel)
