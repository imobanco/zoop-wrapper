from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.invoice import BillingInstructions, Fine, Interest, Discount
from tests.factories.invoice import (
    BillingInstructionsFactory,
    FixedDiscountFactory,
    FixedFineFactory,
    FixedInterestFactory,
)


class BillingInstructionsTestCase(SetTestCase):
    def test_get_non_required_fields(self):
        self.assertEqual(
            {"late_fee", "interest", "discount"},
            BillingInstructions.get_non_required_fields(),
        )

    def test_create(self):
        instance = BillingInstructionsFactory()
        self.assertIsInstance(instance, BillingInstructions)

    def test_init_custom_fields_1(self):
        instance = MagicMock(late_fee=None, interest=None, discount=None)

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

    def test_init_custom_fields_2(self):
        instance = MagicMock(late_fee=None, interest=None, discount=None)

        BillingInstructions.init_custom_fields(
            instance,
            interest=FixedInterestFactory().to_dict(),
            discount=FixedDiscountFactory().to_dict(),
        )
        self.assertEqual(instance.late_fee, None)
        self.assertIsInstance(instance.interest, Interest)
        self.assertIsInstance(instance.discount, list)
        self.assertIsInstance(instance.discount[0], Discount)

    def test_init_custom_fields_3(self):
        instance = MagicMock(late_fee=None, interest=None, discount=None)

        BillingInstructions.init_custom_fields(
            instance,
            late_fee=FixedFineFactory().to_dict(),
            discount=FixedDiscountFactory().to_dict(),
        )
        self.assertIsInstance(instance.late_fee, Fine)
        self.assertEqual(instance.interest, None)
        self.assertIsInstance(instance.discount, list)
        self.assertIsInstance(instance.discount[0], Discount)

    def test_init_custom_fields_4(self):
        instance = MagicMock(late_fee=None, interest=None, discount=None)

        BillingInstructions.init_custom_fields(
            instance,
            late_fee=FixedFineFactory().to_dict(),
            interest=FixedInterestFactory().to_dict(),
        )
        self.assertIsInstance(instance.late_fee, Fine)
        self.assertIsInstance(instance.interest, Interest)
        self.assertEqual(instance.discount, None)
