from tests.utils import SetTestCase
from ZoopAPIWrapper.models.transaction import PointOfSale


class PointOfSaleTestCase(SetTestCase):
    def test_non_required_fields(self):
        self.assertEqual(
            {"entry_mode", 'identification_number'},
            PointOfSale.get_non_required_fields()
        )
