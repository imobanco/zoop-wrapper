from unittest import TestCase

from ZoopAPIWrapper.models.base import OwnerModel, AddressModel


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
            },
        }

    def test_from_dict(self):
        instance = OwnerModel.from_dict(self.data)

        self.assertIsInstance(instance, OwnerModel)
        self.assertEqual(instance.first_name, 'foo')
        self.assertIsInstance(instance.address, AddressModel)
        self.assertEqual(instance.address.city, 'foo')

    def test_to_dict(self):
        instance = OwnerModel.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
