from tests.utils import SetTestCase
from zoop_wrapper.models.invoice import Fine
from tests.factories.invoice import FixedFineFactory


class FineTestCase(SetTestCase):
    def test_modes(self):
        fixed = "FIXED"
        percentage = "PERCENTAGE"

        self.assertEqual(Fine.FIXED, fixed)
        self.assertEqual(Fine.PERCENTAGE, percentage)

        modes = {fixed, percentage}

        self.assertSetEqual(Fine.MODES, modes)

    def test_get_mode_required_fields_mapping(self):
        instance: Fine = FixedFineFactory()

        expected = {
            instance.FIXED: instance.get_fixed_required_fields,
            instance.PERCENTAGE: instance.get_percentage_required_fields,
        }

        result = instance.get_mode_required_fields_mapping()

        self.assertEqual(result, expected)

    def test_non_required_fields(self):
        expected = {"start_date"}

        result = Fine.get_non_required_fields()

        self.assertSetEqual(result, expected)
