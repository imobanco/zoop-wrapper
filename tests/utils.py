from unittest import TestCase
from unittest.mock import patch, MagicMock

from requests import Response
from zoop_wrapper.wrapper import ZoopWrapper

from zoop_wrapper.utils import convert_currency_float_value_to_cents
from zoop_wrapper.exceptions import FieldError


class SetTestCase(TestCase):
    @staticmethod
    def __get_msg(container, contained):
        return (
            f"\n\nset {container} does not contains {contained}.\n\n"
            f"Excess: {contained - container}"
        )

    def assertIsSubSet(self, contained: set, container: set):
        self.assertTrue(
            contained.issubset(container), msg=self.__get_msg(container, contained)
        )


class APITestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.patcher_delete = patch("zoop_wrapper.wrapper.base.requests.delete")
        self.patcher_get = patch("zoop_wrapper.wrapper.base.requests.get")
        self.patcher_post = patch("zoop_wrapper.wrapper.base.requests.post")
        self.patcher_put = patch("zoop_wrapper.wrapper.base.requests.put")

        self.mocked_delete = self.patcher_delete.start()
        self.mocked_get = self.patcher_get.start()
        self.mocked_post = self.patcher_post.start()
        self.mocked_put = self.patcher_put.start()

        self.addCleanup(self.patcher_delete.stop)
        self.addCleanup(self.patcher_get.stop)
        self.addCleanup(self.patcher_post.stop)
        self.addCleanup(self.patcher_put.stop)

        self.client = ZoopWrapper(marketplace_id="foo", key="foo")

    def tearDown(self):
        super().tearDown()
        del self.client

    @staticmethod
    def build_response_mock(status_code=200, content=None):
        response = MagicMock(
            status_code=status_code,
            json=MagicMock(return_value=content if content else {}),
            instance=None,
        )

        def raise_for_status():
            Response.raise_for_status(response)

        response.raise_for_status = raise_for_status
        return response

    def set_get_mock(self, status_code=200, content=None):
        self.mocked_get.return_value = self.build_response_mock(
            status_code=status_code, content=content
        )

    def set_post_mock(self, status_code=200, content=None):
        self.mocked_post.return_value = self.build_response_mock(
            status_code=status_code, content=content
        )

    def set_delete_mock(self, status_code=200, content=None):
        self.mocked_delete.return_value = self.build_response_mock(
            status_code=status_code, content=content
        )


class UtilsTestCase(TestCase):
    def test_convert_currency_float_value_to_cents_int_input(self):
        value = 1234
        expected = 1234
        result = convert_currency_float_value_to_cents(value)
        self.assertEqual(expected, result)

    def test_convert_currency_float_value_to_cents_float_input(self):
        value = 56.78
        expected = 5678
        result = convert_currency_float_value_to_cents(value)
        self.assertEqual(expected, result)

    def test_convert_currency_float_value_to_cents_str_with_int_input(self):
        value = "9876"
        expected = 9876
        result = convert_currency_float_value_to_cents(value)
        self.assertEqual(expected, result)

    def test_convert_currency_float_value_to_cents_str_with_float_input(self):
        value = "91.23"
        expected = 91.23
        result = convert_currency_float_value_to_cents(value)
        self.assertEqual(expected, result)

    def test_convert_currency_float_value_to_cents_none_input(self):
        value = None
        self.assertRaises(FieldError, convert_currency_float_value_to_cents, value)

    def test_convert_currency_float_value_to_cents_random_str_input(self):
        value = "random"
        self.assertRaises(FieldError, convert_currency_float_value_to_cents, value)
