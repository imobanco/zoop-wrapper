from unittest import TestCase

from ZoopAPIWrapper.models.seller import IndividualSeller, Address


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
        instance = IndividualSeller.from_dict(data)

        self.assertIsInstance(instance, IndividualSeller)
        self.assertEqual(instance.id, 'foo')
        self.assertEqual(instance.marketplace_id, 'foo')
        self.assertEqual(instance.type, 'foo')
        self.assertEqual(instance.first_name, 'foo')
        self.assertIsInstance(instance.address, Address)
        self.assertEqual(instance.address.city, 'foo')

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
                "city": "S\u00e3o Paulo",
                "state": "SP",
                "postal_code": "04047002",
                "country_code": "BR"
            },
        }
        instance = IndividualSeller.from_dict(data)

        self.assertIsInstance(instance, IndividualSeller)
        self.assertEqual(instance.to_dict(), data)
