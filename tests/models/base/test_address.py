from tests.utils import MockedAddressLoggerTestCase as TestCase
from ZoopAPIWrapper.models.base import AddressModel
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

    def test_required_fields(self):
        fields = set()
        self.assertTrue(
            fields.issuperset(AddressModel.get_required_fields())
        )

    def test_non_required_fields(self):
        fields = {"line1", "line2", "line3",
                  "neighborhood", "city", "state",
                  "postal_code", "country_code"}
        self.assertTrue(
            fields.issuperset(AddressModel.get_non_required_fields())
        )

    def test_create(self):
        instance = AddressModelFactory()
        self.assertIsInstance(instance, AddressModel)

    def test_from_dict(self):
        instance = AddressModel.from_dict(self.data)

        self.assertIsInstance(instance, AddressModel)
        self.assertEqual(instance.line1, 'foo')
        self.assertEqual(instance.line2, 'foo')
        self.assertEqual(instance.line3, 'foo')
        self.assertEqual(instance.neighborhood, 'foo')
        self.assertEqual(instance.city, 'foo')
        self.assertEqual(instance.state, 'foo')
        self.assertEqual(instance.postal_code, 'foo')
        self.assertEqual(instance.country_code, 'foo')

    def test_to_dict(self):
        instance = AddressModel.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
