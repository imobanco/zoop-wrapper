from unittest.mock import MagicMock

from pycpfcnpj import gen
from factory.faker import Faker

from ..utils import SetTestCase
from ..factories.token import (
    CardTokenFactory,
    CreateCardTokenFactory,
    BankAccountTokenFactory,
    CreateIndividualBankAccountTokenFactory,
    CreateBusinessBankAccountTokenFactory,
)
from ..factories.card import CardFactory
from ..factories.bank_account import IndividualBankAccountFactory
from zoop_wrapper.models.bank_account import BankAccount
from zoop_wrapper.models.card import Card
from zoop_wrapper.models.token import Token
from zoop_wrapper.exceptions import ValidationError, FieldError


class TokenTestCase(SetTestCase):
    def test_init_custom_fields_with_type_raise(self):
        """
        TODO: documentar
        """
        instance = MagicMock(TYPES={"foo"}, _allow_empty=False)

        self.assertRaises(
            ValidationError, Token.init_custom_fields, instance, type="bar"
        )

    def test_init_custom_fields_with_card(self):
        instance = MagicMock(TYPES={"card"}, CARD_TYPE="card")

        Token.init_custom_fields(instance, type="card", card=CardFactory())
        self.assertEqual(instance.token_type, "card")
        self.assertIsInstance(instance.card, Card)

    def test_init_custom_fields_with_allow_empty(self):
        """
        Nesse cenário o Token é usado como se fosse
        um cartão recebendo seus dados juntamente do id.

        Dado um cartão c1 (previamente já criado noa Zoop)
        Quando for criado um Token(id=c1.id, allow_empty=True) t1
        Então o t1.token_type deve ser None
        """
        c1 = MagicMock(id="1")

        instance = MagicMock(TYPES={"card"}, CARD_TYPE="card", _allow_empty=True)

        Token.init_custom_fields(instance, id=c1.id)
        self.assertEqual(instance.token_type, None)

    def test_init_custom_fields_with_bank_account(self):
        instance = MagicMock(TYPES={"bank_account"}, BANK_ACCOUNT_TYPE="bank_account")

        Token.init_custom_fields(
            instance, type="bank_account", bank_account=IndividualBankAccountFactory()
        )
        self.assertEqual(instance.token_type, "bank_account")
        self.assertIsInstance(instance.bank_account, BankAccount)

    def test_init_custom_fields_card(self):
        """
        We set the CARD_IDENTIFIER to 'foo'
        and pass foo='bar' on args!
        """
        instance = MagicMock(CARD_IDENTIFIER="foo",)

        Token.init_custom_fields(instance, foo="bar")
        self.assertEqual(instance.token_type, instance.CARD_TYPE)

    def test_init_custom_fields_bank_account_business(self):
        """
        We set the BANK_ACCOUNT_IDENTIFIER to 'foo'
        and pass foo='bar' on args!
        We must pass 'ein' or 'taxpayer_id' too
        """
        instance = MagicMock(BANK_ACCOUNT_IDENTIFIER="foo")

        cnpj = gen.cnpj()
        Token.init_custom_fields(instance, foo="bar", ein=cnpj)
        self.assertEqual(instance.token_type, instance.BANK_ACCOUNT_TYPE)
        self.assertEqual(instance.ein, cnpj)

    def test_init_custom_fields_bank_account_individual(self):
        instance = MagicMock(BANK_ACCOUNT_IDENTIFIER="foo")

        cpf = gen.cpf()
        Token.init_custom_fields(instance, foo="bar", taxpayer_id=cpf)
        self.assertEqual(instance.token_type, instance.BANK_ACCOUNT_TYPE)
        self.assertEqual(instance.taxpayer_id, cpf)

    def test_validate_custom_fields_card(self):
        """
        Dado que está sendo criado um token de cartão t1 com número de cartão válido
        Quando for chamado t1.validate_custom_fields(**kwargs)
        Então a lista de erros deve estar vazia
        """

        instance: Token = MagicMock(
            card_number=Faker("credit_card_number").generate(),
            token_type=Token.CARD_TYPE,
            CARD_TYPE=Token.CARD_TYPE
        )

        errors = Token.validate_custom_fields(instance)

        self.assertEqual(len(errors), 0)

    def test_validate_custom_fields_card_raise(self):
        """
        Dado que está sendo criado um token de cartão t1 com número de cartão inválido
        Quando for chamado t1.validate_custom_fields(**kwargs)
        Então a lista de erros deve ter um elemento com as mensagens corretas
        """

        instance: Token = MagicMock(
            card_number="123",
            token_type=Token.CARD_TYPE,
            CARD_TYPE=Token.CARD_TYPE
        )

        result = Token.validate_custom_fields(instance)

        self.assertEqual(len(result), 1)
        error = result[0]
        self.assertIsInstance(error, FieldError)
        self.assertEqual(error.name, "card_number")
        self.assertEqual(error.reason, "O número do cartão é inválido!")

    def test_get_non_required_fields(self):
        self.assertIsSubSet({"type", "used"}, Token.get_non_required_fields())

    def test_get_card_non_required_fields(self):
        self.assertIsSubSet({"card"}, Token.get_card_non_required_fields())

    def test_get_card_required_fields(self):
        self.assertIsSubSet(
            {"card_number", "security_code"}, Token.get_card_required_fields()
        )

    def test_get_bank_account_non_required_fields(self):
        self.assertIsSubSet(
            {"bank_account"}, Token.get_bank_account_non_required_fields()
        )

    def test_get_bank_account_required_fields(self):
        self.assertIsSubSet(
            {"account_number"}, Token.get_bank_account_required_fields()
        )

    def test_create_card(self):
        instance = CardTokenFactory(allow_empty=True)
        self.assertIsInstance(instance, Token)

    def test_create_card_create(self):
        instance = CreateCardTokenFactory()
        self.assertIsInstance(instance, Token)

    def test_create_bank_account(self):
        instance = BankAccountTokenFactory(allow_empty=True)
        self.assertIsInstance(instance, Token)

    def test_create_bank_account_create_individual(self):
        instance = CreateIndividualBankAccountTokenFactory()
        self.assertIsInstance(instance, Token)

    def test_create_bank_account_create_business(self):
        instance = CreateBusinessBankAccountTokenFactory()
        self.assertIsInstance(instance, Token)

    def test_get_validation_fields_card(self):
        instance = CardTokenFactory(allow_empty=True)
        self.assertIsInstance(instance, Token)

        self.assertEqual(
            {
                "card_number",
                "expiration_month",
                "expiration_year",
                "holder_name",
                "security_code",
            },
            instance.get_validation_fields(),
        )

    def test_get_validation_fields_bank_account_individual(self):
        instance = BankAccountTokenFactory(allow_empty=True)
        self.assertIsInstance(instance, Token)

        self.assertEqual(
            {
                "account_number",
                "bank_code",
                "holder_name",
                "routing_number",
                "taxpayer_id",
                "type",
            },
            instance.get_validation_fields(),
        )

    def test_get_validation_fields_bank_account_create_business(self):
        instance = CreateBusinessBankAccountTokenFactory()
        self.assertIsInstance(instance, Token)

        self.assertEqual(
            {
                "account_number",
                "bank_code",
                "ein",
                "holder_name",
                "routing_number",
                "type",
            },
            instance.get_validation_fields(),
        )

    def test_get_all_fields_card(self):
        instance = CardTokenFactory(allow_empty=True)
        self.assertIsInstance(instance, Token)

        self.assertIsSubSet({"used", "type", "card"}, instance.get_all_fields())

    def test_get_all_fields_card_create(self):
        instance = CreateCardTokenFactory()
        self.assertIsInstance(instance, Token)

        self.assertIsSubSet(
            {
                "card",
                "card_number",
                "expiration_month",
                "expiration_year",
                "holder_name",
                "security_code",
                "type",
                "used",
            },
            instance.get_all_fields(),
        )

    def test_get_all_fields_bank_account(self):
        instance = BankAccountTokenFactory(allow_empty=True)
        self.assertIsInstance(instance, Token)

        self.assertIsSubSet({"used", "type", "bank_account"}, instance.get_all_fields())

    def test_get_all_fields_bank_account_create_individual(self):
        instance = CreateIndividualBankAccountTokenFactory()
        self.assertIsInstance(instance, Token)

        self.assertIsSubSet(
            {
                "account_number",
                "bank_account",
                "bank_code",
                "holder_name",
                "routing_number",
                "taxpayer_id",
                "type",
                "type",
                "used",
            },
            instance.get_all_fields(),
        )

    def test_get_all_fields_bank_account_create_business(self):
        instance = CreateBusinessBankAccountTokenFactory()
        self.assertIsInstance(instance, Token)

        self.assertIsSubSet(
            {
                "account_number",
                "bank_account",
                "bank_code",
                "ein",
                "holder_name",
                "routing_number",
                "type",
                "type",
                "used",
            },
            instance.get_all_fields(),
        )
