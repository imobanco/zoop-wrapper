from tests.utils import SetTestCase
from zoop_wrapper.models.invoice import Interest
from tests.factories.invoice import FixedInterestFactory


class InterestTestCase(SetTestCase):
    def test_modes(self):
        daily_amount = "DAILY_AMOUNT"
        daily_percentage = "DAILY_PERCENTAGE"
        monthly_percentage = "MONTHLY_PERCENTAGE"

        self.assertEqual(Interest.DAILY_AMOUNT, daily_amount)
        self.assertEqual(Interest.DAILY_PERCENTAGE, daily_percentage)
        self.assertEqual(Interest.MONTHLY_PERCENTAGE, monthly_percentage)

        modes = {daily_amount, daily_percentage, monthly_percentage}

        self.assertSetEqual(Interest.MODES, modes)

    def test_get_mode_required_fields_mapping(self):
        instance: Interest = FixedInterestFactory()

        expected = {
            instance.DAILY_AMOUNT: instance.get_fixed_required_fields,
            instance.DAILY_PERCENTAGE: instance.get_percentage_required_fields,
            instance.MONTHLY_PERCENTAGE: instance.get_percentage_required_fields,
        }

        result = instance.get_mode_required_fields_mapping()

        self.assertEqual(result, expected)

    def test_non_required_fields(self):
        expected = {"start_date"}

        result = Interest.get_non_required_fields()

        self.assertSetEqual(result, expected)
