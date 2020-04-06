from unittest.mock import Mock, MagicMock, PropertyMock

from tests.utils import SetTestCase
from ZoopAPIWrapper.models.bank_account import BankAccount
from ZoopAPIWrapper.models.card import Card
from ZoopAPIWrapper.models.token import Token
from tests.factories.token import (
    CardTokenFactory, CreateCardTokenFactory,
    BankAccountTokenFactory, CreateIndividualBankAccountTokenFactory,
    CreateBusinessBankAccountTokenFactory
)
from tests.factories.card import CardFactory
from tests.factories.bank_account import IndividualBankAccountFactory


class TokenTestCase(SetTestCase):
    def test_init_custom_fields_raise(self):
        instance = MagicMock()

        self.assertRaises(TypeError, Token.init_custom_fields, instance)

    def test_init_custom_fields_with_type_raise(self):
        """
        If there's type and is not in TYPES raise TypeError!
        are not passed raise
        """
        instance = MagicMock(
            TYPES={'foo'}
        )

        self.assertRaises(
            TypeError, Token.init_custom_fields,
            instance, type='bar')

    def test_init_custom_fields_with_card(self):
        instance = MagicMock(
            TYPES={'card'},
            CARD_TYPE='card'
        )

        Token.init_custom_fields(
            instance, type='card',
            card=CardFactory())
        self.assertEqual(instance.token_type, 'card')
        self.assertIsInstance(instance.card, Card)

    def test_init_custom_fields_with_bank_account(self):
        instance = MagicMock(
            TYPES={'bank_account'},
            BANK_ACCOUNT_TYPE='bank_account'
        )

        Token.init_custom_fields(
            instance, type='bank_account',
            bank_account=IndividualBankAccountFactory())
        self.assertEqual(instance.token_type, 'bank_account')
        self.assertIsInstance(instance.bank_account, BankAccount)

    def test_init_custom_fields_card(self):
        """We set the CARD_IDENTIFIER to 'foo'
        and pass foo='bar' on args!"""
        instance = MagicMock(
            CARD_IDENTIFIER='foo',
        )

        Token.init_custom_fields(instance, foo='bar')
        self.assertEqual(instance.token_type, instance.CARD_TYPE)

    def test_init_custom_fields_bank_account_business(self):
        """We set the BANK_ACCOUNT_IDENTIFIER to 'foo'
        and pass foo='bar' on args!
        We must pass 'ein' or 'taxpayer_id' too"""
        instance = MagicMock(
            BANK_ACCOUNT_IDENTIFIER='foo'
        )

        Token.init_custom_fields(instance, foo='bar', ein='foo')
        self.assertEqual(instance.token_type, instance.BANK_ACCOUNT_TYPE)
        self.assertEqual(instance.ein, 'foo')

    def test_init_custom_fields_bank_account_individual(self):
        instance = MagicMock(
            BANK_ACCOUNT_IDENTIFIER='foo',
            TYPE_ATTR='token_type'
        )

        Token.init_custom_fields(instance, foo='bar', taxpayer_id='foo')
        self.assertEqual(instance.token_type, instance.BANK_ACCOUNT_TYPE)
        self.assertEqual(instance.taxpayer_id, 'foo')

    def test_get_type_raise(self):
        instance = Mock(spec=['IDENTIFIERS'])

        self.assertRaises(TypeError, Token.get_type, instance)

    def test_get_type_card(self):
        instance = MagicMock(
            token_type=Token.CARD_TYPE
        )

        token_type = Token.get_type(instance)
        self.assertEqual(token_type, Token.CARD_TYPE)

    def test_get_type_bank_account(self):
        instance = MagicMock(
            token_type=Token.BANK_ACCOUNT_TYPE
        )

        token_type = Token.get_type(instance)
        self.assertEqual(token_type, Token.BANK_ACCOUNT_TYPE)

    def test_get_non_required_fields(self):
        self.assertIsSubSet(
            {'type', 'used'},
            Token.get_non_required_fields()
        )

    def test_get_card_non_required_fields(self):
        self.assertIsSubSet(
            {'card'},
            Token.get_card_non_required_fields()
        )

    def test_get_card_required_fields(self):
        self.assertIsSubSet(
            {'card_number', 'security_code'},
            Token.get_card_required_fields()
        )

    def test_get_bank_account_non_required_fields(self):
        self.assertIsSubSet(
            {'bank_account'},
            Token.get_bank_account_non_required_fields()
        )

    def test_get_bank_account_required_fields(self):
        self.assertIsSubSet(
            {'account_number'},
            Token.get_bank_account_required_fields()
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
            {'security_code', 'expiration_year', 'card_number',
             'holder_name', 'expiration_month'},
            instance.get_validation_fields()
        )

    def test_get_validation_fields_bank_account_individual(self):
        instance = BankAccountTokenFactory(allow_empty=True)
        self.assertIsInstance(instance, Token)

        self.assertEqual(
            {'holder_name', 'type', 'account_number',
             'taxpayer_id', 'bank_code', 'routing_number'},
            instance.get_validation_fields()
        )

    def test_get_validation_fields_bank_account_create_business(self):
        instance = CreateBusinessBankAccountTokenFactory()
        self.assertIsInstance(instance, Token)

        self.assertEqual(
            {'holder_name', 'type', 'account_number',
             'ein', 'bank_code', 'routing_number'},
            instance.get_validation_fields()
        )

    def test_get_all_fields_card(self):
        instance = CardTokenFactory(allow_empty=True)
        self.assertIsInstance(instance, Token)

        self.assertIsSubSet(
            {'used', 'type', 'card'},
            instance.get_all_fields()
        )

    def test_get_all_fields_card_create(self):
        instance = CreateCardTokenFactory()
        self.assertIsInstance(instance, Token)

        self.assertIsSubSet(
            {'type', 'used', 'security_code', 'expiration_year',
             'card_number', 'holder_name', 'expiration_month', 'card'},
            instance.get_all_fields()
        )

    def test_get_all_fields_bank_account(self):
        instance = BankAccountTokenFactory(allow_empty=True)
        self.assertIsInstance(instance, Token)

        self.assertIsSubSet(
            {'used', 'type', 'bank_account'},
            instance.get_all_fields()
        )

    def test_get_all_fields_bank_account_create_individual(self):
        instance = CreateIndividualBankAccountTokenFactory()
        self.assertIsInstance(instance, Token)

        self.assertIsSubSet(
            {'used', 'type', 'bank_account', 'holder_name',
             'type', 'account_number',
             'taxpayer_id', 'bank_code', 'routing_number'},
            instance.get_all_fields()
        )

    def test_get_all_fields_bank_account_create_business(self):
        instance = CreateBusinessBankAccountTokenFactory()
        self.assertIsInstance(instance, Token)

        self.assertIsSubSet(
            {'used', 'type', 'bank_account', 'holder_name',
             'type', 'account_number',
             'ein', 'bank_code', 'routing_number'},
            instance.get_all_fields()
        )
