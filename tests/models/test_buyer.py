from unittest.mock import MagicMock, patch

from tests.utils import SetTestCase
from zoop_wrapper.models.buyer import Buyer
from zoop_wrapper.models.base import Address
from tests.factories.buyer import BuyerFactory
from zoop_wrapper.exceptions import FieldError


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

    def test_validate_custom_fields(self):
        instance: Buyer = BuyerFactory()

        result = Buyer.validate_custom_fields(instance)

        self.assertEqual(len(result), 0)

    def test_validate_custom_fields_empty(self):
        instance: Buyer = BuyerFactory(allow_empty=True)

        result = Buyer.validate_custom_fields(instance)

        self.assertEqual(len(result), 0)

    def test_validate_custom_fields_raise(self):
        instance: Buyer = MagicMock(_allow_empty=False, taxpayer_id=123)

        result = Buyer.validate_custom_fields(instance)

        self.assertEqual(len(result), 1)

        error: FieldError = result[0]
        self.assertIsInstance(error, FieldError)
        self.assertEqual(error.name, "taxpayer_id")
        self.assertIn("taxpayer_id inválido!", error.reason)

    def test_init_custom_fields(self):
        instance: Buyer = MagicMock()

        Buyer.init_custom_fields(instance)
        self.assertIsInstance(instance.address, Address)
