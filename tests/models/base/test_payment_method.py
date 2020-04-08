from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.base import PaymentMethod, Address
from tests.factories.base import (
    PaymentMethodFactory)


class PaymentMethodTestCase(SetTestCase):
    def test_non_required_fields(self):
        self.assertIsSubSet(
            {'description', 'address', 'customer'},
            PaymentMethod.get_non_required_fields()
        )

    def test_create(self):
        instance = PaymentMethodFactory()
        self.assertIsInstance(instance, PaymentMethod)

    def test_init_custom_fields(self):
        instance = MagicMock()

        PaymentMethod.init_custom_fields(instance)
        self.assertIsInstance(instance.address, Address)
