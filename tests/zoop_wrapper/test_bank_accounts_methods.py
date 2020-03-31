from unittest.mock import patch, MagicMock

from tests.utils import RequestsMockedTestCase
from ZoopAPIWrapper.wrapper import ZoopWrapper
from ZoopAPIWrapper.models.bank_account import BankAccount
from ZoopAPIWrapper.models.factories.bank_account import (
    BankAccountFactory, IndividualBankAccountFactory)
from ZoopAPIWrapper.models.factories.token import TokenFactory
from ZoopAPIWrapper.models.factories.seller import IndividualSellerFactory


class ZoopWrapperBankAccountsMethodsTestCase(RequestsMockedTestCase):
    def setUp(self):
        super().setUp()
        self.client = ZoopWrapper()

    def tearDown(self):
        del self.client

    def test_list_bank_accounts(self):
        """
        Test list_bank_accounts method.
        """
        self.set_get_mock(
            200,
            {'items': [IndividualBankAccountFactory().to_dict()]}
        )
        response = self.client.list_bank_accounts()
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get('items')
        self.assertTrue(items)

    def test_retrieve_bank_account(self):
        """
        Test retrieve_bank_account method.
        """
        self.set_get_mock(
            200,
            IndividualBankAccountFactory(
                id='foo'
            ).to_dict()
        )
        response = self.client.retrieve_bank_account('foo')
        self.assertEqual(response.status_code, 200, msg=response.data)
        data = response.data
        self.assertEqual(data.get('id'), 'foo', msg=data)
        self.assertIsInstance(response.instance, BankAccount)
        self.assertEqual(response.instance.id, 'foo')

    def test_add_bank_account_token(self):
        """
        Test __add_token method.
        """
        self.set_post_mock(
            201,
            TokenFactory().to_dict()
        )

        bank_account = BankAccountFactory()

        response = self.client.\
            _ZoopWrapper__add_token(bank_account)
        self.assertEqual(response.status_code, 201, msg=response.data)

    @patch('ZoopAPIWrapper.wrapper.ZoopWrapper._ZoopWrapper__add_token')
    def test_add_bank_account(self, mocked_add_token):
        """
        Test add_bank_account method.
        """
        mocked_add_token.return_value = MagicMock(
            instance=TokenFactory()
        )

        data = IndividualBankAccountFactory(
            id='foo'
        ).to_dict()

        self.set_post_mock(
            200,
            data
        )

        self.set_get_mock(
            200,
            IndividualSellerFactory(
                id='foo',
                taxpayer_id='bar'
            ).to_dict()
        )

        response = self.client.add_bank_account(data)
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(data.get('id'), 'foo', msg=data)
        self.assertIsInstance(response.instance, BankAccount)
        self.assertEqual(response.instance.id, 'foo')
