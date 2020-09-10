from unittest.mock import MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.transaction import Source
from tests.factories.token import CreateCardTokenFactory
from tests.factories.source import SourceCardPresentFactory, SourceCardNotPresentFactory
from tests.factories.installment_plan import InstallmentPlanFactory

from zoop_wrapper.models.token import Token
from zoop_wrapper.exceptions import ValidationError


class SourceTestCase(SetTestCase):
    def test_init_custom_fields_with_source_type_wrong(self):

        instance = MagicMock(SOURCE_TYPES={"foo"})

        self.assertRaises(
            ValidationError,
            Source.init_custom_fields,
            instance,
            amount=1234,
            type="bar",
        )

    def test_init_custom_fields_card_present_type(self):
        """
        Dado:
            - Um cartão qualquer válido c1
            - Um installment_plan qualquer válido ip1
            - usage="single_use"
            - amount=1234
        Quando:
            - for chamado Source.init_custom_fields( ...)
        Então:
            - Nenhum erro deve ocorrer
            - instance.card deve ser uma instância de Token
        """
        c1 = CreateCardTokenFactory()
        ip1 = InstallmentPlanFactory()

        instance = MagicMock()

        Source.init_custom_fields(
            instance, card=c1, usage="single_use", amount=1234, installment_plan=ip1,
        )

        self.assertIsInstance(instance.card, Token)

    def test_init_custom_fields_card_present_type_installment_plan_raise(self):
        """
        Dado:
            - Um installment_plan inválido installment_plan_invalid
        Quando:
            - for chamado Source.init_custom_fields( ..., installment_plan=installment_plan_invalid) # noqa
        Então:
            - O erro ValidationError deve ser lançado

        Note:
            - O number_installments só pode ser de 1 até 12
            - O mode só pode ser ou with_interest ou interest_free
        """

        installment_plan_invalid = MagicMock(mode="foo-bar", number_installments=11234)

        instance = MagicMock()

        with self.assertRaises(ValidationError):
            Source.init_custom_fields(
                instance,
                card=CreateCardTokenFactory(),
                usage="single_use",
                amount=1234,
                installment_plan=installment_plan_invalid,
            )

    def test_required_fields(self):

        self.assertEqual(
            {"card", "type", "usage", "currency", "amount", "installment_plan"},
            Source.get_required_fields(),
        )

    def test_create_card_present(self):
        instance = SourceCardPresentFactory()
        self.assertIsInstance(instance, Source)

    def test_create_card_not_present(self):
        instance = SourceCardNotPresentFactory(
            card=CreateCardTokenFactory(id="123"), usage="single_use", amount="567"
        )
        self.assertIsInstance(instance, Source)

    def test_get_card_not_present_required_fields(self):
        self.assertEqual(
            {"card", "type", "amount", "usage", "currency", "installment_plan"},
            Source.get_card_not_present_required_fields(),
        )

    def test_get_card_present_required_fields(self):
        self.assertEqual(
            {"amount", "card", "currency", "type", "usage", "installment_plan"},
            Source.get_card_present_required_fields(),
        )

    def test_get_validation_fields_card_not_present(self):
        instance = SourceCardNotPresentFactory(
            card=CreateCardTokenFactory(id="123"), usage="single_use", amount="500"
        )
        self.assertIsInstance(instance, Source)

        self.assertEqual(
            {"card", "type", "currency", "usage", "amount", "installment_plan"},
            instance.get_validation_fields(),
        )

    def test_get_all_fields_card_not_present(self):
        instance = SourceCardNotPresentFactory(
            card=CreateCardTokenFactory(id="123"), usage="single_use", amount="500"
        )
        self.assertIsInstance(instance, Source)
        self.assertEqual(
            {"card", "currency", "type", "usage", "amount", "installment_plan"},
            instance.get_all_fields(),
        )

    def test_get_validation_fields_card_present(self):
        instance = SourceCardPresentFactory(card=CreateCardTokenFactory(id=None))
        self.assertIsInstance(instance, Source)

        self.assertEqual(
            {"card", "type", "usage", "currency", "amount", "installment_plan"},
            instance.get_validation_fields(),
        )

    def test_get_all_fields_card_present(self):
        instance = SourceCardPresentFactory(card=CreateCardTokenFactory(id=None))
        self.assertIsInstance(instance, Source)
        self.assertEqual(
            {"card", "type", "usage", "currency", "amount", "installment_plan"},
            instance.get_all_fields(),
        )
