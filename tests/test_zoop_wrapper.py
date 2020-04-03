from unittest.mock import patch, MagicMock

from tests.utils import APITestCase
from ZoopAPIWrapper.wrapper import ZOOP_KEY


class ZoopWrapperTestCase(APITestCase):
    def test_auth(self):
        self.assertEqual(self.client._auth, (ZOOP_KEY, ''))

    @patch('ZoopAPIWrapper.wrapper.RequestsWrapper._post')
    @patch('ZoopAPIWrapper.wrapper.isinstance')
    def test_post_instance(self, mocked_isinstance, mocked_post):
        instance = MagicMock()
        self.assertIsInstance(instance, MagicMock)

        self.client._post_instance('bla', instance)

        instance.to_dict.assert_called_once()

        self.assertIsInstance(mocked_post, MagicMock)
        mocked_post.assert_called_once_with('bla', data=instance.to_dict())
