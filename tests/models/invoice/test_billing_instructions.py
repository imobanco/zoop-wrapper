from tests.utils import SetTestCase
from ZoopAPIWrapper.models.invoice import (
    BillingInstructions, BillingConfiguration
)
from ZoopAPIWrapper.models.factories.invoice import (
    BillingInstructionsFactory
)


class BillingInstructionsTestCase(SetTestCase):
    @property
    def data(self):
        return {
            'late_fee': {
                "mode": BillingConfiguration.FIXED_MODE,
                "amount": 'foo',
                "start_date": 'foo'
            },
            'interest': {
                "mode": BillingConfiguration.FIXED_MODE,
                "amount": 'foo',
                "start_date": 'foo'
            },
            'discount': {
                "mode": BillingConfiguration.FIXED_MODE,
                "amount": 'foo',
                "limit_date": 'foo'
            }
        }

    def test_get_required_fields(self):
        self.assertIsSuperSet(
            {'late_fee', 'interest', 'discount'},
            BillingInstructions.get_required_fields()
        )

    def test_create(self):
        instance = BillingInstructionsFactory()
        self.assertIsInstance(instance, BillingInstructions)

    def test_from_dict(self):
        instance = BillingInstructions.from_dict(self.data)

        self.assertIsInstance(instance, BillingInstructions)

        self.assertIsInstance(instance.late_fee, BillingConfiguration)
        self.assertEqual(instance.late_fee.mode, BillingConfiguration.FIXED_MODE)
        self.assertEqual(instance.late_fee.amount, 'foo')
        self.assertEqual(instance.late_fee.start_date, 'foo')

        self.assertIsInstance(instance.interest, BillingConfiguration)
        self.assertEqual(instance.interest.mode, BillingConfiguration.FIXED_MODE)
        self.assertEqual(instance.interest.amount, 'foo')
        self.assertEqual(instance.interest.start_date, 'foo')

        self.assertIsInstance(instance.discount, BillingConfiguration)
        self.assertEqual(instance.discount.mode, BillingConfiguration.FIXED_MODE)
        self.assertEqual(instance.discount.amount, 'foo')
        self.assertEqual(instance.discount.limit_date, 'foo')

    def test_to_dict(self):
        instance = BillingInstructions.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
