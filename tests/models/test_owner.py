from unittest import TestCase

from ZoopAPIWrapper.models import Owner, Address


class OwnerTestCase(TestCase):
    def test_from_dict(self):
        data = {
            "first_name": "foo",
            "last_name": "foo",
            "email": "foo",
            "taxpayer_id": "foo",
            "phone_number": "foo",
            "birthdate": 'foo',
            "address": {
                "line1": "Avenida Senador Casimiro da Rocha",
                "line2": "1000",
                "line3": "de 0741/742 a 1095/1096",
                "neighborhood": "Mirand\u00f3polis",
                "city": "foo",
                "state": "SP",
                "postal_code": "04047002",
                "country_code": "BR"
            },
        }
        instance = Owner.from_dict(data)

        self.assertIsInstance(instance, Owner)
        self.assertEqual(instance.first_name, 'foo')
        self.assertIsInstance(instance.address, Address)
        self.assertEqual(instance.address.city, 'foo')

    def test_to_dict(self):
        data = {
            "first_name": "foo",
            "last_name": "foo",
            "email": "foo",
            "taxpayer_id": "foo",
            "phone_number": "foo",
            "birthdate": 'foo',
            "address": {
                "line1": "Avenida Senador Casimiro da Rocha",
                "line2": "1000",
                "line3": "de 0741/742 a 1095/1096",
                "neighborhood": "Mirand\u00f3polis",
                "city": "foo",
                "state": "SP",
                "postal_code": "04047002",
                "country_code": "BR"
            },
        }
        instance = Owner.from_dict(data)

        self.assertIsInstance(instance, Owner)
        self.assertEqual(instance.to_dict(), data)
