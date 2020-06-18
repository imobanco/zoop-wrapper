from tests.utils import SetTestCase
from zoop_wrapper.models.base import FinancialModel
from tests.factories.base import FinancialModelFactory


class FinancialTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertEqual(set(), FinancialModel.get_required_fields())

    def test_non_required_fields(self):
        self.assertEqual(
            {
                "account_balance",
                "current_balance",
                "default_credit",
                "default_debit",
                "delinquent",
                "description",
                "payment_methods",
                "status",
            },
            FinancialModel.get_non_required_fields(),
        )

    def test_create(self):
        instance = FinancialModelFactory()
        self.assertIsInstance(instance, FinancialModel)
