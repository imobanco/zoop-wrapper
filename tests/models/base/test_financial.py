from tests.utils import SetTestCase
from ZoopAPIWrapper.models.base import FinancialModel
from ZoopAPIWrapper.models.factories.base import FinancialModelFactory


class FinancialTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertIsSuperSet(
            set(),
            FinancialModel.get_required_fields()
        )

    def test_non_required_fields(self):
        self.assertIsSuperSet(
            {'status', 'account_balance', 'current_balance',
             'description', 'delinquent', 'payment_methods',
             'default_debit', 'default_credit'},
            FinancialModel.get_non_required_fields()
        )

    def test_create(self):
        instance = FinancialModelFactory()
        self.assertIsInstance(instance, FinancialModel)
