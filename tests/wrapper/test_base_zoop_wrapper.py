from unittest.mock import patch, MagicMock

from tests.utils import APITestCase
from zoop_wrapper.wrapper.base import BaseZoopWrapper
from zoop_wrapper.exceptions import ValidationError


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

    def test_post_instance_raise(self):
        instance = MagicMock()
        self.assertIsInstance(instance, MagicMock)

        with self.assertRaises(ValidationError):
            self.client._post_instance("bla", instance)

    @patch("zoop_wrapper.wrapper.base.RequestsWrapper._put")
    def test_put_instance(self, mocked_put):
        instance = MagicMock()
        self.assertIsInstance(instance, MagicMock)

        with patch("zoop_wrapper.wrapper.base.isinstance"):
            self.client._put_instance("bla", instance)

        instance.to_dict.assert_called_once()

        self.assertIsInstance(mocked_put, MagicMock)
        mocked_put.assert_called_once_with("bla", data=instance.to_dict())

    def test_put_instance_raise(self):
        instance = MagicMock()
        self.assertIsInstance(instance, MagicMock)

        with self.assertRaises(ValidationError):
            self.client._put_instance("bla", instance)
