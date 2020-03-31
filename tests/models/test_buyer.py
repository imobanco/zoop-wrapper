from tests.utils import SetTestCase
from ZoopAPIWrapper.models.buyer import Buyer
from ZoopAPIWrapper.models.base import Address
from ZoopAPIWrapper.models.factories.buyer import BuyerFactory


class BuyerTestCase(SetTestCase):
    @property
    def data(self):
        return {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
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

    def test_non_required_fields(self):
        self.assertIsSubSet(
            {"default_receipt_delivery_method", 'marketplace_id',
             'resource'},
            Buyer.get_non_required_fields()
        )

    def test_create(self):
        instance = BuyerFactory()
        self.assertIsInstance(instance, Buyer)

    def test_from_dict(self):
        instance = Buyer.from_dict(self.data)

        self.assertIsInstance(instance, Buyer)
        self.assertEqual(instance.first_name, 'foo')
        self.assertIsInstance(instance.address, Address)

    def test_to_dict(self):
        data = self.data

        instance = Buyer.from_dict(data)

        data.pop('default_receipt_delivery_method')

        self.assertEqual(instance.to_dict(), data)
