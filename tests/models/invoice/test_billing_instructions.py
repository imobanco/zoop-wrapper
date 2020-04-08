from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.invoice import (
    BillingInstructions, BillingConfiguration
)
from tests.factories.invoice import (
    BillingInstructionsFactory
)


class BillingInstructionsTestCase(SetTestCase):
    def test_get_required_fields(self):
        self.assertEqual(
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
        self.assertIsInstance(instance.discount, list)
        self.assertIsInstance(instance.discount[0], BillingConfiguration)
