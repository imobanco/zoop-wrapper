from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.base import Person, Address
from tests.factories.base import PersonFactory
from zoop_wrapper.exceptions import FieldError


class PersonTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertEqual(
            {
                "address",
                "email",
                "first_name",
                "last_name",
                "phone_number",
                "taxpayer_id",
            },
            Person.get_required_fields(),
        )

    def test_non_required_fields(self):
        self.assertEqual({"birthdate"}, Person.get_non_required_fields())

    def test_create(self):
        instance = PersonFactory()
        self.assertIsInstance(instance, Person)

    def test_full_name(self):
        instance = PersonFactory(first_name="foo", last_name="bar")
        self.assertIsInstance(instance, Person)

        self.assertEqual(instance.full_name, "foo bar")

    def test_init_custom_fields(self):
        instance = MagicMock()

        Person.init_custom_fields(instance)
        self.assertIsInstance(instance.address, Address)

    def test_validate_custom_fields(self):
        """
        Testa o Person.validate_custom_fields.

        Dado que existe person p1
        Quando for chamado p1.validate_custom_fields()
        Então deve ter sido retornado uma lista vazia
        """

        p1: Person = PersonFactory()

        result = p1.validate_custom_fields()

        self.assertEqual(len(result), 0)

    def test_validate_custom_fields_empty(self):
        """
        Testa o Person.validate_custom_fields.

        Dado que existe person p1 com `taxpeyr_id` inválido e `allow_empty=True`
        Quando for chamado p1.validate_custom_fields()
        Então deve ter sido retornado uma lista vazia
        """
        p1: Person = PersonFactory(allow_empty=True, taxpayer_id=123)

        result = p1.validate_custom_fields()

        self.assertEqual(len(result), 0)

    def test_validate_custom_fields_raise(self):
        """
        Testa o Person.validate_custom_fields.

        Dado que existe person p1 com `taxpeyr_id` inválido e `allow_empty=False`
        Quando for chamado p1.validate_custom_fields()
        Então deve ter sido retornado uma lista com 1 erro de taxpayer_id
        """
        p1: Person = MagicMock(_allow_empty=False, taxpayer_id=123)

        result = Person.validate_custom_fields(p1)

        self.assertEqual(len(result), 1)

        error: FieldError = result[0]
        self.assertIsInstance(error, FieldError)
        self.assertEqual(error.name, "taxpayer_id")
        self.assertIn("taxpayer_id inválido!", error.reason)
