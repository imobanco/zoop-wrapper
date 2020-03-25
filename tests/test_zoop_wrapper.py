from unittest import TestCase
from unittest.mock import patch, MagicMock

from ZoopAPIWrapper.wrapper import ZoopWrapper, ZOOP_KEY


class ZoopWrapperTestCase(TestCase):
    def test_auth(self):
        zw = ZoopWrapper()
        self.assertEqual(zw._auth, (ZOOP_KEY, ''))

    @patch('ZoopAPIWrapper.wrapper.RequestsWrapper._post')
    @patch('ZoopAPIWrapper.wrapper.isinstance')
    def test_post_instance(self, mocked_isinstance, mocked_post):
        instance = MagicMock()
        self.assertIsInstance(instance, MagicMock)

        zw = ZoopWrapper()
        zw._post_instance('bla', instance)

        instance.to_dict.assert_called_once()

        self.assertIsInstance(mocked_post, MagicMock)
        mocked_post.assert_called_once_with('bla', data=instance.to_dict())
