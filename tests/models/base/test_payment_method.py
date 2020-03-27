from unittest import TestCase

from ZoopAPIWrapper.models.base import PaymentMethod, AddressModel
from ZoopAPIWrapper.models.factories.base import (
    PaymentMethodFactory)


class PaymentMethodTestCase(TestCase):
    @property
    def data(self):
        return {
            'description': 'foo',
            'customer': 'foo',
            'address': {
                "line1": 'foo',
                "line2": 'foo',
                "line3": 'foo',
                "neighborhood": 'foo',
                "city": 'foo',
                "state": 'foo',
                "postal_code": 'foo',
                "country_code": 'foo'
            }
        }

    def test_required_fields(self):
        fields = {'description', 'customer', 'address'}
        self.assertTrue(
            fields.issuperset(PaymentMethod.get_required_fields())
        )

    def test_non_required_fields(self):
        fields = set()
        self.assertTrue(
            fields.issubset(PaymentMethod.get_non_required_fields())
        )

    def test_create(self):
        instance = PaymentMethodFactory()
        self.assertIsInstance(instance, PaymentMethod)

    def test_from_dict(self):
        instance = PaymentMethod.from_dict(self.data)

        self.assertIsInstance(instance, PaymentMethod)
        self.assertEqual(instance.description, 'foo')
        self.assertEqual(instance.customer, 'foo')
        self.assertIsInstance(instance.address, AddressModel)

    def test_to_dict(self):
        instance = PaymentMethod.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
