from tests.utils import MockedAddressLoggerTestCase as TestCase, SetTestCase
from ZoopAPIWrapper.models.base import Person, Address
from ZoopAPIWrapper.models.factories.base import PersonFactory


class PersonTestCase(TestCase, SetTestCase):
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
        self.assertIsSuperSet(
            {"first_name", "last_name", "email",
             "taxpayer_id", "phone_number",
             "birthdate", "address"},
            Person.get_required_fields()
        )

    def test_non_required_fields(self):
        self.assertIsSuperSet(
            set(),
            Person.get_non_required_fields()
        )

    def test_create(self):
        instance = PersonFactory()
        self.assertIsInstance(instance, Person)

    def test_from_dict(self):
        instance = Person.from_dict(self.data)

        self.assertIsInstance(instance, Person)
        self.assertEqual(instance.first_name, 'foo')
        self.assertIsInstance(instance.address, Address)
        self.assertEqual(instance.address.city, 'foo')

    def test_to_dict(self):
        instance = Person.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)

    def test_full_name(self):
        instance = PersonFactory(first_name='foo', last_name='bar')
        self.assertIsInstance(instance, Person)

        self.assertEqual(instance.full_name, 'foo bar')
