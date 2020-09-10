from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.invoice import BillingInstructions, Fine, Interest, Discount
from tests.factories.invoice import (
    BillingInstructionsFactory,
    FixedFineFactory,
    FixedInterestFactory,
    FixedDiscountFactory,
)


class BillingInstructionsTestCase(SetTestCase):
    def test_get_required_fields(self):
        self.assertEqual(
            {"late_fee", "interest", "discount"},
            BillingInstructions.get_required_fields(),
        )

    def test_create(self):
        instance = BillingInstructionsFactory()
        self.assertIsInstance(instance, BillingInstructions)

    def test_init_custom_fields(self):
        instance = MagicMock()

        BillingInstructions.init_custom_fields(
            instance,
            late_fee=FixedFineFactory().to_dict(),
            interest=FixedInterestFactory().to_dict(),
            discount=FixedDiscountFactory().to_dict(),
        )
        self.assertIsInstance(instance.late_fee, Fine)
        self.assertIsInstance(instance.interest, Interest)
        self.assertIsInstance(instance.discount, list)
        self.assertIsInstance(instance.discount[0], Discount)
