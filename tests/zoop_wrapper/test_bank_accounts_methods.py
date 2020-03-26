from tests.utils import RequestsMockedTestCase
from ZoopAPIWrapper.wrapper import ZoopWrapper
from ZoopAPIWrapper.models.bank_account import BankAccount
from ZoopAPIWrapper.models.factories.bank_account import (
    IndividualBankAccountFactory)


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
