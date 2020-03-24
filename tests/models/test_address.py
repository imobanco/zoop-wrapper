from unittest import TestCase

from ZoopAPIWrapper.models.base import Address


class AddressTestCase(TestCase):
    def test_from_dict(self):
        data = {
            "line1": 'foo',
            "line2": 'foo',
            "line3": 'foo',
            "neighborhood": 'foo',
            "city": 'foo',
            "state": 'foo',
            "postal_code": 'foo',
            "country_code": 'foo'
        }
        instance = Address.from_dict(data)

        self.assertIsInstance(instance, Address)
        self.assertEqual(instance.line1, 'foo')

    def test_to_dict(self):
        data = {
            "line1": 'foo',
            "line2": 'foo',
            "line3": 'foo',
            "neighborhood": 'foo',
            "city": 'foo',
            "state": 'foo',
            "postal_code": 'foo',
            "country_code": 'foo'
        }
        instance = Address.from_dict(data)

        self.assertIsInstance(instance, Address)
        self.assertEqual(instance.to_dict(), data)
