from tests.utils import SetTestCase
from zoop_wrapper.models.invoice import Discount
from tests.factories.invoice import FixedDiscountFactory


class DiscountTestCase(SetTestCase):
    def test_modes(self):
        fixed = "FIXED"
        percentage = "PERCENTAGE"

        self.assertEqual(Discount.FIXED, fixed)
        self.assertEqual(Discount.PERCENTAGE, percentage)

        modes = {fixed, percentage}

        self.assertSetEqual(Discount.MODES, modes)

    def test_get_mode_required_fields_mapping(self):
        instance: Discount = FixedDiscountFactory()

        expected = {
            instance.FIXED: instance.get_fixed_required_fields,
            instance.PERCENTAGE: instance.get_percentage_required_fields,
        }

        result = instance.get_mode_required_fields_mapping()

        self.assertEqual(result, expected)

    def test_required_fields(self):
        expected = {"limit_date", "mode"}

        result = Discount.get_required_fields()

        self.assertSetEqual(result, expected)
