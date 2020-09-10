from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.transaction import InstallmentPlan

from zoop_wrapper.exceptions import FieldError


class InstallmentPlanTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertEqual(
            {"number_installments", "mode"}, InstallmentPlan.get_required_fields(),
        )

    def test_validate_custom_fields_mode_raise(self):
        """
        Testa o InstallmentPlan.validate_custom_fields

        Dado:
            - que existe InstallmentPlan ip1 com `mode` inválido e `number_installments=3` # noqa
        Quando:
            - for chamado ip1.validate_custom_fields()
        Então:
            - deve ter sido retornado uma lista com 1 erro de `mode`
        """
        ip1: InstallmentPlan = MagicMock(mode="foo-bar", number_installments=3)

        result = InstallmentPlan.validate_custom_fields(ip1)

        self.assertEqual(len(result), 1)

        error: FieldError = result[0]
        self.assertIsInstance(error, FieldError)
        self.assertEqual(error.name, "mode")
        self.assertIn("mode é inválido!", error.reason)

    def test_validate_custom_fields_number_installments_raise(self):
        """
        Testa o InstallmentPlan.validate_custom_fields

        Dado:
            - que existe InstallmentPlan ip1 com `mode` válido e
            `number_installments='foo'` inválido
        Quando:
            - for chamado ip1.validate_custom_fields()
        Então:
            - deve ter sido retornado uma lista com 1 erro de `number_installments`
        """
        ip1: InstallmentPlan = MagicMock(
            mode="with_interest",
            number_installments="foo",
            INSTALLMENT_PLAN_MODES=InstallmentPlan.INSTALLMENT_PLAN_MODES,
        )

        result = InstallmentPlan.validate_custom_fields(ip1)

        self.assertEqual(len(result), 1)

        error: FieldError = result[0]

        self.assertIsInstance(error, FieldError)
        self.assertEqual(error.name, "number_installments")
        self.assertIn("number_installments é inválido!", error.reason)

    def test_validate_number_installments_not_int(self):
        """
        Testa o InstallmentPlan._validate_number_installments

        Dado:
            - que existe number_installments com um valor que não é um inteiro
        Quando:
            - for chamado InstallmentPlan._validate_number_installments(number_installments) # noqa
        Então:
            - o retorno deve ser True
        """

        number_installments = "algo-que-não-é-int"

        result = InstallmentPlan._validate_number_installments(number_installments)
        expected = False
        self.assertEqual(result, expected)

    def test_validate_number_installments_less_than_one(self):
        """
        Testa o InstallmentPlan._validate_number_installments

        Dado:
            - que existe number_installments com um valor menor do que 1
        Quando:
            - for chamado InstallmentPlan._validate_number_installments(number_installments) # noqa
        Então:
            - o retorno deve ser True
        """

        number_installments = 0

        result = InstallmentPlan._validate_number_installments(number_installments)
        expected = False
        self.assertEqual(result, expected)

    def test_validate_number_installments_greater_than_12(self):
        """
        Testa o InstallmentPlan._validate_number_installments

        Dado:
            - que existe number_installments com um valor menor do que 1
        Quando:
            - for chamado InstallmentPlan._validate_number_installments(number_installments) # noqa
        Então:
            - o retorno deve ser True
        """

        number_installments = 13

        result = InstallmentPlan._validate_number_installments(number_installments)
        expected = False
        self.assertEqual(result, expected)
