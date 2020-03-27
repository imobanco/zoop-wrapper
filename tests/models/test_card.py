from unittest import TestCase

from ZoopAPIWrapper.models.card import Card, CardVerificationChecklist
from ZoopAPIWrapper.models.factories.card import (
    CardFactory
)


class CardTestCase(TestCase):
    @property
    def data(self):
        return {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

            'description': 'foo',
            'customer': 'foo',
            'address': {
                "line1": 'foo',
                "line2": 'foo',
                "line3": 'foo',
                "neighborhood": 'foo',
                "city": 'foo',
                "state": 'foo',
                "postal_code": 'foo',
                "country_code": 'foo'
            },

            "card_brand": 'foo',
            "first4_digits": 'foo',
            "last4_digits": 'foo',
            "expiration_month": 'foo',
            "expiration_year": 'foo',
            "holder_name": 'foo',
            "is_active": 'foo',
            "is_valid": 'foo',
            "is_verified": 'foo',
            "fingerprint": 'foo',
            "verification_checklist": {
                "postal_code_check": 'foo',
                "address_line1_check": 'foo',

                "security_code_check": 'foo'
            }
        }

    def test_create(self):
        instance = CardFactory()
        self.assertIsInstance(instance, Card)

    def test_from_dict(self):
        instance = Card.from_dict(self.data)

        self.assertIsInstance(instance, Card)
        self.assertEqual(instance.card_brand, 'foo')
        self.assertEqual(instance.first4_digits, 'foo')
        self.assertIsInstance(instance.verification_checklist, CardVerificationChecklist)

    def test_to_dict(self):
        instance = Card.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
