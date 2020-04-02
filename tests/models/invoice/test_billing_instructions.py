from unittest.mock import MagicMock

from tests.utils import SetTestCase
from ZoopAPIWrapper.models.invoice import (
    BillingInstructions, BillingConfiguration
)
from tests.factories import (
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

    def test_init_custom_fields(self):
        instance = MagicMock()

        BillingInstructions.init_custom_fields(instance)
        self.assertIsInstance(instance.late_fee, BillingConfiguration)
        self.assertIsInstance(instance.interest, BillingConfiguration)
        self.assertIsInstance(instance.discount, BillingConfiguration)
