from unittest.mock import MagicMock, patch

from tests.utils import SetTestCase
from zoop_wrapper.models.buyer import Buyer
from zoop_wrapper.models.base import Address
from tests.factories.buyer import BuyerFactory


class BuyerTestCase(SetTestCase):
    def test_non_required_fields(self):
        self.assertIsSubSet(
            {"default_receipt_delivery_method", "marketplace_id", "resource"},
            Buyer.get_non_required_fields(),
        )

        with patch(
            "zoop_wrapper.models.base.MarketPlaceModel.get_non_required_fields"
        ) as mocked_get_non_required_fields:
            Buyer.get_non_required_fields()
            mocked_get_non_required_fields.assert_called_once()

    def test_create(self):
        instance = BuyerFactory()
        self.assertIsInstance(instance, Buyer)

    def test_init_custom_fields(self):
        instance = MagicMock()

        Buyer.init_custom_fields(instance)
        self.assertIsInstance(instance.address, Address)
