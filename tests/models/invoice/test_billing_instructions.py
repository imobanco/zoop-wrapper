from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.invoice import BillingInstructions, Fine, Interest, Discount
from tests.factories.invoice import (
    BillingInstructionsFactory,
    FixedDiscountFactory,
    FixedFineFactory,
    FixedInterestFactory,
)


class BillingInstructionsTestCase(SetTestCase):
    def test_get_non_required_fields(self):
        self.assertEqual(
            {"late_fee", "interest", "discount"},
            BillingInstructions.get_non_required_fields(),
        )

    def test_create(self):
        instance = BillingInstructionsFactory()
        self.assertIsInstance(instance, BillingInstructions)

    def test_init_custom_fields_1(self):
        """
        Serve para testar a inicialização correta dos campos!

        Dado que existe uma instância mocada
        Quando for inicializado os campos:
            - late_fee com dados válidos
            - interest com dados válidos
            - discount com dados válidos
        Então:
            - instância.late_fee deve ser válido
            - instância.interest deve ser válido
            - instância.discount deve ser válido
        """
        instance = MagicMock(late_fee=None, interest=None, discount=None)

        BillingInstructions.init_custom_fields(
            instance,
            late_fee=FixedFineFactory().to_dict(),
            interest=FixedInterestFactory().to_dict(),
            discount=FixedDiscountFactory().to_dict(),
        )
        self.assertIsInstance(instance.late_fee, Fine)
        self.assertIsInstance(instance.interest, Interest)
        self.assertIsInstance(instance.discount, list)
        self.assertIsInstance(instance.discount[0], Discount)

    def test_init_custom_fields_2(self):
        """
        Serve para testar a flexibilização do campo late_fee!

        Dado que existe uma instância mocada
        Quando forem inicializados os campos:
            - interest com dados válidos
            - discount com dados válidos
        Então:
            - instância.interest deve ser válido
            - instância.discount deve ser válido
        """
        instance = MagicMock(late_fee=None, interest=None, discount=None)

        BillingInstructions.init_custom_fields(
            instance,
            interest=FixedInterestFactory().to_dict(),
            discount=FixedDiscountFactory().to_dict(),
        )
        self.assertEqual(instance.late_fee, None)
        self.assertIsInstance(instance.interest, Interest)
        self.assertIsInstance(instance.discount, list)
        self.assertIsInstance(instance.discount[0], Discount)

    def test_init_custom_fields_3(self):
        """
        Serve para testar a flexibilização do campo interest!

        Dado que existe uma instância mocada
        Quando forem inicializados os campos:
            - late_fee com dados válidos
            - discount com dados válidos
        Então:
            - instância.late_fee deve ser válido
            - instância.discount deve ser válido
        """
        instance = MagicMock(late_fee=None, interest=None, discount=None)

        BillingInstructions.init_custom_fields(
            instance,
            late_fee=FixedFineFactory().to_dict(),
            discount=FixedDiscountFactory().to_dict(),
        )
        self.assertIsInstance(instance.late_fee, Fine)
        self.assertEqual(instance.interest, None)
        self.assertIsInstance(instance.discount, list)
        self.assertIsInstance(instance.discount[0], Discount)

    def test_init_custom_fields_4(self):
        """
        Serve para testar a flexibilização do campo discount!

        Dado que existe uma instância mocada
        Quando for inicializado os campos:
            - late_fee com dados válidos
            - interest com dados válidos
        Então:
            - instância.late_fee deve ser válido
            - instância.interest deve ser válido
        """
        instance = MagicMock(late_fee=None, interest=None, discount=None)

        BillingInstructions.init_custom_fields(
            instance,
            late_fee=FixedFineFactory().to_dict(),
            interest=FixedInterestFactory().to_dict(),
        )
        self.assertIsInstance(instance.late_fee, Fine)
        self.assertIsInstance(instance.interest, Interest)
        self.assertEqual(instance.discount, None)
