from unittest.mock import patch, MagicMock

from tests.utils import APITestCase
from zoop_wrapper.wrapper.base import BaseZoopWrapper


class ZoopWrapperTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.client = BaseZoopWrapper(key="foo")

    def test_auth(self):
        self.assertEqual(self.client._auth, ("foo", ""))

    @patch("zoop_wrapper.wrapper.base.RequestsWrapper._post")
    def test_post_instance(self, mocked_post):
        instance = MagicMock()
        self.assertIsInstance(instance, MagicMock)

        with patch("zoop_wrapper.wrapper.base.isinstance"):
            self.client._post_instance("bla", instance)

        instance.to_dict.assert_called_once()

        self.assertIsInstance(mocked_post, MagicMock)
        mocked_post.assert_called_once_with("bla", data=instance.to_dict())
