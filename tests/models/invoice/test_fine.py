from unittest.mock import patch, MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.exceptions import ValidationError
from zoop_wrapper.models.invoice import Fine
from tests.factories.invoice import (
    FixedFineFactory,
    PercentageFineFactory
)


class FineTestCase(SetTestCase):
    def test_modes(self):
        fixed = 'FIXED'
        percentage = 'PERCENTAGE'

        self.assertEqual(Fine.FIXED, fixed)
        self.assertEqual(Fine.PERCENTAGE, percentage)

        modes = {fixed, percentage}

        self.assertSetEqual(Fine.MODES, modes)

    def test_required_fields(self):
        expected = {'mode'}

        result = Fine.get_required_fields()

        self.assertSetEqual(result, expected)

    def test_fixed_required_fields(self):
        expected = {'amount', 'mode'}

        result = Fine.get_fixed_required_fields()

        self.assertSetEqual(result, expected)

    def test_percentage_required_fields(self):
        expected = {'percentage', 'mode'}

        result = Fine.get_percentage_required_fields()

        self.assertSetEqual(result, expected)

    def test_non_required_fields(self):
        expected = {'start_date'}

        result = Fine.get_non_required_fields()

        self.assertSetEqual(result, expected)

    def test_init_custom_fields_1(self):
        """
        Dado que:
            - existe um objeto instance com mode=None
        Quando for chamado Fine.init_custom_fields(instance, mode=Fine.FIXED)
        Então instance.mode deve ser Fine.FIXED
        """
        instance = MagicMock(mode=None)

        self.assertEqual(instance.mode, None)

        Fine.init_custom_fields(instance, mode=Fine.FIXED)

        self.assertEqual(instance.mode, Fine.FIXED)

    def test_init_custom_fields_2(self):
        """
        Dado que:
            - existe um objeto instance com mode=None
        Quando for chamado Fine.init_custom_fields(instance, mode=Fine.PERCENTAGE)
        Então instance.mode deve ser Fine.PERCENTAGE
        """
        instance = MagicMock(mode=None)

        self.assertEqual(instance.mode, None)

        Fine.init_custom_fields(instance, mode=Fine.PERCENTAGE)

        self.assertEqual(instance.mode, Fine.PERCENTAGE)

    def test_init_custom_fields_3(self):
        """
        Dado que:
            - existe um objeto instance com mode=None
        Quando for chamado Fine.init_custom_fields(instance, mode='foo')
        Então deve ser levantado um ValidationError
        """
        instance = MagicMock(mode=None)

        self.assertEqual(instance.mode, None)

        with self.assertRaises(ValidationError):
            Fine.init_custom_fields(instance, mode='foo')

        self.assertEqual(instance.mode, None)

    def test_get_validation_fields_1(self):
        """
        Dado que:
            - existe uma multa f1 de porcentagem
        Quando for chamado f1.get_validation_fields()
        Deve ser retornado {'percentage', 'mode'}
        """
        f1: Fine = PercentageFineFactory()

        expected = {'percentage', 'mode'}

        result = f1.get_validation_fields()

        self.assertSetEqual(result, expected)

    def test_get_validation_fields_2(self):
        """
        Dado que:
            - existe uma multa f1 de valor fixo
        Quando for chamado f1.get_validation_fields()
        Deve ser retornado {'amount', 'mode'}
        """
        f1: Fine = FixedFineFactory()

        expected = {'amount', 'mode'}

        result = f1.get_validation_fields()

        self.assertSetEqual(result, expected)

    def test_get_all_fields_1(self):
        """
        Dado que:
            - existe uma multa f1 de porcentagem
        Quando for chamado f1.get_all_fields()
        Deve ser retornado {'percentage', 'mode', 'start_date'}
        """
        f1: Fine = PercentageFineFactory()

        expected = {'percentage', 'mode', 'start_date'}

        result = f1.get_all_fields()

        self.assertSetEqual(result, expected)

    def test_get_all_fields_2(self):
        """
        Dado que:
            - existe uma multa f1 de valor fixo
        Quando for chamado f1.get_all_fields()
        Deve ser retornado {'amount', 'mode', 'start_date'}
        """
        f1: Fine = FixedFineFactory()

        expected = {'amount', 'mode', 'start_date'}

        result = f1.get_all_fields()

        self.assertSetEqual(result, expected)
