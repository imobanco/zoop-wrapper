from tests.utils import SetTestCase
from ZoopAPIWrapper.models.token import Token
from tests.factories.token import TokenFactory


class TokenTestCase(SetTestCase):
    def test_get_non_required_fields(self):
        self.assertIsSubSet(
            {'type', 'used'},
            Token.get_non_required_fields()
        )

    def test_create(self):
        instance = TokenFactory()
        self.assertIsInstance(instance, Token)
