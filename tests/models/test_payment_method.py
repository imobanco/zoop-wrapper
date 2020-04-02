from unittest import TestCase

from ZoopAPIWrapper.models.base import PaymentMethod, Address
from ZoopAPIWrapper.models.factories.base import (
    PaymentMethodFactory)


class PaymentMethodTestCase(TestCase):
    @property
    def data(self):
        return {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

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

    def test_create(self):
        instance = PaymentMethodFactory()
        self.assertIsInstance(instance, PaymentMethod)

    def test_from_dict(self):
        instance = PaymentMethod.from_dict(self.data)

        self.assertIsInstance(instance, PaymentMethod)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.resource, 'foo')
        self.assertEqual(instance.uri, 'foo')
        self.assertEqual(instance.description, 'foo')
        self.assertEqual(instance.customer, 'foo')
        self.assertIsInstance(instance.address, Address)

    def test_to_dict(self):
        instance = PaymentMethod.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
