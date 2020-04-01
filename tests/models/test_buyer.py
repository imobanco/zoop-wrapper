from tests.utils import SetTestCase
from ZoopAPIWrapper.models.buyer import Buyer
from ZoopAPIWrapper.models.base import Address
from ZoopAPIWrapper.models.factories.buyer import BuyerFactory


class BuyerTestCase(SetTestCase):
    def test_non_required_fields(self):
        self.assertIsSubSet(
            {"default_receipt_delivery_method", 'marketplace_id',
             'resource'},
            Buyer.get_non_required_fields()
        )

    def test_create(self):
        instance = BuyerFactory()
        self.assertIsInstance(instance, Buyer)
