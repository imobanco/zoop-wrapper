from unittest import TestCase

from zoop_wrapper.utils import convert_currency_float_value_to_cents
from zoop_wrapper.exceptions import FieldError


class UtilsTestCase(TestCase):
    def test_convert_currency_float_value_to_cents_int_input(self):
        """
        Dado:
            - um valor 1234
        Quando:
            - for chamado convert_currency_float_value_to_cents(value)
        Então:
            - o resultado deve ser 1234
        """
        value = 1234
        expected = 1234
        result = convert_currency_float_value_to_cents(value)
        self.assertEqual(expected, result)

    def test_convert_currency_float_value_to_cents_float_input(self):
        """
        Dado:
            - um valor 56.78123123123123123
        Quando:
            - for chamado convert_currency_float_value_to_cents(value)
        Então:
            - o resultado deve ser 5678
        """
        value = 56.78123123123123123
        expected = 5678
        result = convert_currency_float_value_to_cents(value)
        self.assertEqual(expected, result)

    def test_convert_currency_float_value_to_cents_float_input_1(self):
        """
        Dado:
            - um valor 56.7
        Quando:
            - for chamado convert_currency_float_value_to_cents(value)
        Então:
            - o resultado deve ser 5670
        """
        value = 56.7
        expected = 5670
        result = convert_currency_float_value_to_cents(value)
        self.assertEqual(expected, result)

    def test_convert_currency_float_value_to_cents_float_input_2(self):
        """
        Dado:
            - um valor 653.55
        Quando:
            - for chamado convert_currency_float_value_to_cents(value)
        Então:
            - o resultado deve ser 65355
        """
        value = 653.55
        expected = 65355
        result = convert_currency_float_value_to_cents(value)
        self.assertEqual(expected, result)

    def test_convert_currency_float_value_to_cents_str_with_int_input(self):
        """
        Dado:
            - um valor "9876"
        Quando:
            - for chamado convert_currency_float_value_to_cents(value)
        Então:
            - o resultado deve ser 9876
        """
        value = "9876"
        expected = 9876
        result = convert_currency_float_value_to_cents(value)
        self.assertEqual(expected, result)

    def test_convert_currency_float_value_to_cents_str_with_float_input(self):
        """
        Dado:
            - um valor "91.23"
        Quando:
            - for chamado convert_currency_float_value_to_cents(value)
        Então:
            - o resultado deve ser 9123
        """
        value = "91.23"
        expected = 9123
        result = convert_currency_float_value_to_cents(value)
        self.assertEqual(expected, result)

    def test_convert_currency_float_value_to_cents_none_input(self):
        """
        Dado:
            - um valor None
        Quando:
            - for chamado convert_currency_float_value_to_cents(value)
        Então:
            - deve ser lançado um FieldError
        """
        value = None
        with self.assertRaises(FieldError):
            convert_currency_float_value_to_cents(value)

    def test_convert_currency_float_value_to_cents_random_str_input(self):
        """
        Dado:
            - um valor "random"
        Quando:
            - for chamado convert_currency_float_value_to_cents(value)
        Então:
            - deve ser lançado um FieldError
        """
        value = "random"
        with self.assertRaises(FieldError):
            convert_currency_float_value_to_cents(value)
