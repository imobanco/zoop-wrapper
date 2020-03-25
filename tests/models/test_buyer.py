from unittest import TestCase

from ZoopAPIWrapper.models.buyer import Buyer
from ZoopAPIWrapper.models.base import AddressModel


class BuyerTestCase(TestCase):
    @property
    def data(self):
        return {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

            'marketplace_id': 'foo',

            "status": 'foo',
            "account_balance": 'foo',
            "current_balance": 'foo',
            "delinquent": 'foo',
            "payment_methods": 'foo',
            "default_debit": 'foo',
            "default_credit": 'foo',

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

            "default_receipt_delivery_method": None
        }

    def test_from_dict(self):
        instance = Buyer.from_dict(self.data)

        self.assertIsInstance(instance, Buyer)
        self.assertEqual(instance.first_name, 'foo')
        self.assertIsInstance(instance.address, AddressModel)

    def test_to_dict(self):
        data = self.data

        instance = Buyer.from_dict(data)

        data.pop('default_receipt_delivery_method')

        self.assertEqual(instance.to_dict(), data)
