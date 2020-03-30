from tests.utils import SetTestCase
from ZoopAPIWrapper.models.token import Token
from ZoopAPIWrapper.models.factories.token import TokenFactory


class TokenTestCase(SetTestCase):
    @property
    def data(self):
        return {
            'id': 'foo',
            'resource': 'foo',
            'uri': 'foo',
            'metadata': {},
            'created_at': 'foo',
            'updated_at': 'foo',

            "used": False,
            "type": 'foo'
        }

    def test_get_non_required_fields(self):
        self.assertIsSubSet(
            {'type', 'used'},
            Token.get_non_required_fields()
        )

    def test_create(self):
        instance = TokenFactory()
        self.assertIsInstance(instance, Token)

    def test_from_dict(self):
        instance = Token.from_dict(self.data)

        self.assertIsInstance(instance, Token)
        self.assertEqual(instance.id, 'foo')
        self.assertFalse(instance.used)
        self.assertEqual(instance.type, 'foo')

    def test_to_dict(self):
        instance = Token.from_dict(self.data)

        self.assertEqual(instance.to_dict(), self.data)
