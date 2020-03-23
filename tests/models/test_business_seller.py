from unittest import TestCase

from ZoopAPIWrapper.models import BusinessSeller, Owner, Address


class IndividualSellerTestCase(TestCase):
    def test_from_dict(self):
        data = {
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
        instance = BusinessSeller.from_dict(data)

        self.assertIsInstance(instance, BusinessSeller)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.marketplace_id, 'foo')
        self.assertEqual(instance.type, 'foo')
        self.assertEqual(instance.business_name, 'foo')
        self.assertIsInstance(instance.business_address, Address)
        self.assertEqual(instance.business_address.city, 'foo')
        self.assertIsInstance(instance.owner, Owner)
        self.assertEqual(instance.owner.first_name, 'foo')

    def test_to_dict(self):
        data = {
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
        instance = BusinessSeller.from_dict(data)

        self.assertIsInstance(instance, BusinessSeller)
        self.assertEqual(instance.to_dict(), data)
