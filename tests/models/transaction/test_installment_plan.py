from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.transaction import InstallmentPlan


class InstallmentPlanTestCase(SetTestCase):

    def test_required_fields(self):
        self.assertEqual(
            {"with_interest", "interest_free"},
            InstallmentPlan.get_required_fields(),
        )
