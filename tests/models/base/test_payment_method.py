from tests.utils import SetTestCase
from ZoopAPIWrapper.models.base import PaymentMethod, Address
from ZoopAPIWrapper.models.factories.base import (
    PaymentMethodFactory)


class PaymentMethodTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertIsSuperSet(
            {'customer', 'address'},
            PaymentMethod.get_required_fields()
        )

    def test_non_required_fields(self):
        self.assertIsSubSet(
            {'description'},
            PaymentMethod.get_non_required_fields()
        )

    def test_create(self):
        instance = PaymentMethodFactory()
        self.assertIsInstance(instance, PaymentMethod)
