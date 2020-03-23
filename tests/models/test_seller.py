from unittest import TestCase

from ZoopAPIWrapper.models.seller import Seller, BusinessSeller, IndividualSeller, Owner, Address


class SellerTestCase(TestCase):
    def test_get_class_from_type(self):
        individual_klass = Seller.get_seller_class('individual')
        self.assertEqual(individual_klass, IndividualSeller)

        business_klass = Seller.get_seller_class('business')
        self.assertEqual(business_klass, BusinessSeller)

        self.assertRaises(ValueError, Seller.get_seller_class, 'test')

    def test_seller_from_dict_business(self):
        data = {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

            'marketplace_id': 'foo',

            "status": 'foo',
            "type": 'business',
            "account_balance": 'foo',
            "current_balance": 'foo',
            "description": 'foo',
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

            "business_name": "foo",
            "business_phone": "foo",
            "business_email": "foo",
            "business_website": "foo",
            "business_description": "foo",
            "business_opening_date": "foo",
            "business_facebook": "foo",
            "business_twitter": "foo",
            "ein": "foo",
            "business_address": {
                "line1": "foo",
                "line2": "foo",
                "line3": "foo",
                "neighborhood": "foo",
                "city": "foo",
                "state": "foo",
                "postal_code": "foo",
                "country_code": "foo"
            },
            "owner": {
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
        }
        instance = Seller.from_dict(data)

        self.assertIsInstance(instance, BusinessSeller)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.marketplace_id, 'foo')
        self.assertEqual(instance.type, 'business')
        self.assertEqual(instance.business_name, 'foo')
        self.assertIsInstance(instance.business_address, Address)
        self.assertEqual(instance.business_address.city, 'foo')
        self.assertIsInstance(instance.owner, Owner)
        self.assertEqual(instance.owner.first_name, 'foo')

    def test_seller_from_dict_individual(self):
        data = {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

            'marketplace_id': 'foo',

            "status": 'foo',
            "type": 'individual',
            "account_balance": 'foo',
            "current_balance": 'foo',
            "description": 'foo',
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

            "first_name": "foo",
            "last_name": "foo",
            "email": "foo",
            "taxpayer_id": "foo",
            "phone_number": "foo",
            "birthdate": 'foo',
            "website": 'foo',
            "facebook": 'foo',
            "twitter": 'foo',
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
        instance = Seller.from_dict(data)

        self.assertIsInstance(instance, IndividualSeller)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.marketplace_id, 'foo')
        self.assertEqual(instance.type, 'individual')
        self.assertEqual(instance.first_name, 'foo')
        self.assertIsInstance(instance.address, Address)
        self.assertEqual(instance.address.city, 'foo')
