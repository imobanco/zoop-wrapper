from unittest import TestCase

from zoop_wrapper.utils import convert_currency_float_value_to_cents
from zoop_wrapper.exceptions import FieldError


class UtilsTestCase(TestCase):
    def test_convert_currency_float_value_to_cents_int_input(self):
        value = 1234
        expected = 1234
        result = convert_currency_float_value_to_cents(value)
        self.assertEqual(expected, result)

    def test_convert_currency_float_value_to_cents_float_input(self):
        value = 56.78123123123123123
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
        expected = 9123
        result = convert_currency_float_value_to_cents(value)
        self.assertEqual(expected, result)

    def test_convert_currency_float_value_to_cents_none_input(self):
        value = None
        self.assertRaises(FieldError, convert_currency_float_value_to_cents, value)

    def test_convert_currency_float_value_to_cents_random_str_input(self):
        value = "random"
        self.assertRaises(FieldError, convert_currency_float_value_to_cents, value)
