from tests.utils import SetTestCase
from zoop_wrapper.models.transaction import InstallmentPlan


class InstallmentPlanTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertEqual(
            {"number_installments", "mode"},
            InstallmentPlan.get_required_fields(),
        )
