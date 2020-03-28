from tests.utils import MockedAddressLoggerTestCase as TestCase
from ZoopAPIWrapper.models.base import OwnerModel, AddressModel
from ZoopAPIWrapper.models.factories.base import OwnerModelFactory


class OwnerModelTestCase(TestCase):
    @property
    def data(self):
        return {
            "first_name": "foo",
            "last_name": "foo",
            "email": "foo",
            "taxpayer_id": "foo",
            "phone_number": "foo",
            "birthdate": 'foo',
            "address": {
                "line1": "foo",
                "line2": "foo",
                "line3": "foo",
                "neighborhood": "foo",
                "city": "foo",
                "state": "foo",
                "postal_code": "foo",
                "country_code": "foo"
            }
        }

    def test_required_fields(self):
        fields = {"first_name", "last_name", "email",
                  "taxpayer_id", "phone_number",
                  "birthdate", "address"}
        self.assertTrue(
            fields.issuperset(OwnerModel.get_required_fields())
        )

    def test_non_required_fields(self):
        fields = set()
        self.assertTrue(
            fields.issuperset(OwnerModel.get_non_required_fields())
        )

    def test_create(self):
        instance = OwnerModelFactory()
        self.assertIsInstance(instance, OwnerModel)

    def test_from_dict(self):
        instance = OwnerModel.from_dict(self.data)

        self.assertIsInstance(instance, OwnerModel)
        self.assertEqual(instance.first_name, 'foo')
        self.assertIsInstance(instance.address, AddressModel)
        self.assertEqual(instance.address.city, 'foo')

    def test_to_dict(self):
        instance = OwnerModel.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)

    def test_full_name(self):
        instance = OwnerModelFactory(first_name='foo', last_name='bar')
        self.assertIsInstance(instance, OwnerModel)

        self.assertEqual(instance.full_name, 'foo bar')