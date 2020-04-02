from unittest.mock import MagicMock

from tests.utils import SetTestCase
from ZoopAPIWrapper.models.buyer import Buyer
from ZoopAPIWrapper.models.base import Address
from tests.factories.buyer import BuyerFactory


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

    def test_init_custom_fields(self):
        instance = MagicMock()

        Buyer.init_custom_fields(instance)
        self.assertIsInstance(instance.address, Address)
