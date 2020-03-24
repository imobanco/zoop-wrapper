from unittest import TestCase

from ZoopAPIWrapper.models.token import Token


class TokenTestCase(TestCase):
    def test_from_dict(self):
        data = {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

            "used": False,
            "type": 'foo'
        }
        instance = Token.from_dict(data)

        self.assertIsInstance(instance, Token)
        self.assertEqual(instance.id, 'foo')
        self.assertFalse(instance.used)
        self.assertEqual(instance.type, 'foo')

    def test_to_dict(self):
        data = {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

            "used": False,
            "type": 'foo'
        }
        instance = Token.from_dict(data)

        self.assertIsInstance(instance, Token)
        self.assertEqual(instance.to_dict(), data)
