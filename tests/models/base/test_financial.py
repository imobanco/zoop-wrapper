from tests.utils import SetTestCase
from ZoopAPIWrapper.models.base import FinancialModel
from ZoopAPIWrapper.models.factories.base import FinancialModelFactory


class FinancialTestCase(SetTestCase):
    @property
    def data(self):
        return {
            "status": 'foo',
            "account_balance": 'foo',
            "current_balance": 'foo',
            "description": 'foo',
            "delinquent": 'foo',
            "payment_methods": 'foo',
            "default_debit": 'foo',
            "default_credit": 'foo',
        }

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

    def test_from_dict(self):
        instance = FinancialModel.from_dict(self.data)

        self.assertIsInstance(instance, FinancialModel)
        self.assertEqual(instance.status, 'foo')
        self.assertEqual(instance.account_balance, 'foo')
        self.assertEqual(instance.current_balance, 'foo')
        self.assertEqual(instance.description, 'foo')
        self.assertEqual(instance.delinquent, 'foo')
        self.assertEqual(instance.default_credit, 'foo')
        self.assertEqual(instance.default_debit, 'foo')

    def test_to_dict(self):
        instance = FinancialModel.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
