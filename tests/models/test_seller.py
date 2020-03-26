from tests.utils import MockedAddressLoggerTestCase as TestCase
from ZoopAPIWrapper.models.seller import (
    Seller, BusinessSeller, IndividualSeller, OwnerModel, AddressModel)
from ZoopAPIWrapper.models.factories.seller import SellerFactory


class SellerTestCase(TestCase):
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
            "type": 'foo',
            "account_balance": 'foo',
            "current_balance": 'foo',
            "statement_descriptor": 'foo',
            "mcc": 'foo',
            "show_profile_online": 'foo',
            "is_mobile": 'foo',
            "decline_on_fail_security_code": 'foo',
            "decline_on_fail_zipcode": 'foo',
            "delinquent": 'foo',
            "payment_methods": 'foo',
            "default_debit": 'foo',
            "default_credit": 'foo',
            "merchant_code": 'foo',
            "terminal_code": 'foo',
        }

    def test_create(self):
        instance = SellerFactory()
        self.assertIsInstance(instance, Seller)

    def test_seller_from_dict_business(self):
        data = self.data
        data["ein"] = "foo"
        data["business_name"] = "foo"
        data["business_phone"] = "foo"
        data["business_email"] = "foo"
        data["business_website"] = "foo"
        data["business_description"] = "foo"
        data["business_opening_date"] = "foo"
        data["business_facebook"] = "foo"
        data["business_twitter"] = "foo"
        data["business_address"] = {
            "line1": "foo",
            "line2": "foo",
            "line3": "foo",
            "neighborhood": "foo",
            "city": "foo",
            "state": "foo",
            "postal_code": "foo",
            "country_code": "foo"
        }
        data["owner"] = {
            "first_name": "foo",
            "last_name": "foo",
            "email": "foo",
            "phone_number": "foo",
            "taxpayer_id": "foo",
            "birthdate": "foo",
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

        instance = Seller.from_dict(data)

        self.assertIsInstance(instance, BusinessSeller)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.marketplace_id, 'foo')
        self.assertEqual(instance.type, 'foo')
        self.assertEqual(instance.business_name, 'foo')
        self.assertIsInstance(instance.business_address, AddressModel)
        self.assertEqual(instance.business_address.city, 'foo')
        self.assertIsInstance(instance.owner, OwnerModel)
        self.assertEqual(instance.owner.first_name, 'foo')

    def test_seller_from_dict_individual(self):
        data = self.data
        data["taxpayer_id"] = "foo"
        data["birthdate"] = "foo"
        data["first_name"] = "foo"
        data["last_name"] = "foo"
        data["phone_number"] = "foo"
        data["email"] = "foo"
        data["website"] = "foo"
        data["description"] = "foo"
        data["facebook"] = "foo"
        data["twitter"] = "foo"
        data["address"] = {
            "line1": "foo",
            "line2": "foo",
            "line3": "foo",
            "neighborhood": "foo",
            "city": "foo",
            "state": "foo",
            "postal_code": "foo",
            "country_code": "foo"
        }

        instance = Seller.from_dict(data)

        self.assertIsInstance(instance, IndividualSeller)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.marketplace_id, 'foo')
        self.assertEqual(instance.type, 'foo')
        self.assertEqual(instance.first_name, 'foo')
        self.assertIsInstance(instance.address, AddressModel)
        self.assertEqual(instance.address.city, 'foo')
