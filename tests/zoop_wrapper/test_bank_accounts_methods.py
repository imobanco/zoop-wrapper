import json

from tests.utils import MockedPostDeleteTestCase
from ZoopAPIWrapper.wrapper import ZoopWrapper
from ZoopAPIWrapper.models.bank_account import BankAccount


class ZoopWrapperBankAccountsMethodsTestCase(MockedPostDeleteTestCase):
    def setUp(self):
        super().setUp()
        self.client = ZoopWrapper()

    def tearDown(self):
        del self.client

    def test_list_bank_accounts(self):
        """
        Test list_bank_accounts method.
        And create a dump with all bank_accounts.
        """
        response = self.client.list_bank_accounts()
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get('items')
        self.assertTrue(items)
        json_object = json.dumps(items, indent=4)
        with open("data/bank_accounts.json", "w") as outfile:
            outfile.write(json_object)

    def test_retrieve_bank_account(self):
        """
        Test retrieve_bank_account method.
        Got this bank_account id from the json dump of bank_accounts.
        """
        response = self.client.retrieve_bank_account(
            '064d3c7846b142e591896d2fb69dac3f')
        self.assertEqual(response.status_code, 200, msg=response.data)
        data = response.data
        self.assertEqual(data.get('id'), '064d3c7846b142e591896d2fb69dac3f',
                         msg=data)
        self.assertIsInstance(response.instance, BankAccount)
        self.assertEqual(response.instance.id,
                         '064d3c7846b142e591896d2fb69dac3f')
