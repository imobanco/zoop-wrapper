from tests.utils import MockedAddressLoggerTestCase as TestCase
from ZoopAPIWrapper.models.base import Address
from ZoopAPIWrapper.models.factories.base import AddressModelFactory


class AddressTestCase(TestCase):
    @property
    def data(self):
        return {
            "line1": 'foo',
            "line2": 'foo',
            "line3": 'foo',
            "neighborhood": 'foo',
            "city": 'foo',
            "state": 'foo',
            "postal_code": 'foo',
            "country_code": 'foo'
        }

    def test_create(self):
        instance = AddressModelFactory()
        self.assertIsInstance(instance, Address)

    def test_from_dict(self):
        instance = Address.from_dict(self.data)

        self.assertIsInstance(instance, Address)
        self.assertEqual(instance.line1, 'foo')
        self.assertEqual(instance.line2, 'foo')
        self.assertEqual(instance.line3, 'foo')
        self.assertEqual(instance.neighborhood, 'foo')
        self.assertEqual(instance.city, 'foo')
        self.assertEqual(instance.state, 'foo')
        self.assertEqual(instance.postal_code, 'foo')
        self.assertEqual(instance.country_code, 'foo')

    def test_to_dict(self):
        instance = Address.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
