from tests.utils import SetTestCase
from ZoopAPIWrapper.models.invoice import (
    BillingInstructions, BillingConfiguration
)
from ZoopAPIWrapper.models.factories.invoice import (
    BillingInstructionsFactory
)


class BillingInstructionsTestCase(SetTestCase):
    def test_get_required_fields(self):
        self.assertIsSuperSet(
            {'late_fee', 'interest', 'discount'},
            BillingInstructions.get_required_fields()
        )

    def test_create(self):
        instance = BillingInstructionsFactory()
        self.assertIsInstance(instance, BillingInstructions)
