from tests.utils import MockedAddressLoggerTestCase as TestCase, SetTestCase
from ZoopAPIWrapper.models.base import Person, Address
from ZoopAPIWrapper.models.factories.base import PersonFactory


class PersonTestCase(TestCase, SetTestCase):
    def test_required_fields(self):
        self.assertIsSuperSet(
            {"first_name", "last_name", "email",
             "taxpayer_id", "phone_number",
             "birthdate", "address"},
            Person.get_required_fields()
        )

    def test_create(self):
        instance = PersonFactory()
        self.assertIsInstance(instance, Person)

    def test_full_name(self):
        instance = PersonFactory(first_name='foo', last_name='bar')
        self.assertIsInstance(instance, Person)

        self.assertEqual(instance.full_name, 'foo bar')
