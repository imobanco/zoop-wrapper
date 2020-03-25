import json
from unittest import TestCase
from unittest.mock import patch, MagicMock

from pycpfcnpj import gen

from ZoopAPIWrapper.wrapper import ZoopWrapper, MARKETPLACE_ID, ZOOP_KEY
from ZoopAPIWrapper.models.seller import BusinessSeller, IndividualSeller
from ZoopAPIWrapper.models.bank_account import BankAccount


class ZoopTestCase(TestCase):
    def setUp(self):
        self.client = ZoopWrapper()

    def tearDown(self):
        del self.client

    def test_list_sellers(self):
        """
        Test list_sellers method.
        And create a dump with all sellers.
        """
        response = self.client.list_sellers()
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get('items')
        self.assertTrue(items)
        json_object = json.dumps(items, indent=4)
        with open("data/sellers.json", "w") as outfile:
            outfile.write(json_object)

    def test_retrieve_seller(self):
        """
        Test retrieve_seller method.
        Got this seller id from the json dump of sellers.
        """
        response = self.client.retrieve_seller(
            '27e17b778b404a83bf8e25ec995e2ffe')
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get('id'),
                         '27e17b778b404a83bf8e25ec995e2ffe')
        self.assertIsInstance(response.instance, BusinessSeller)
        self.assertEqual(response.instance.id,
                         '27e17b778b404a83bf8e25ec995e2ffe')

    def test_search_individual_seller(self):
        """
        Test search_individual_seller method.
        Got this seller taxpayer_id from the json dump of sellers.
        """
        response = self.client.search_individual_seller('12685293892')
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get('id'),
                         '29f1251bc7514b96ad5f6d873f9812a1')
        self.assertIsInstance(response.instance, IndividualSeller)
        self.assertEqual(response.instance.id,
                         '29f1251bc7514b96ad5f6d873f9812a1')

    def test_search_business_seller(self):
        """
        Test search_business_seller method.
        Got this seller taxpayer_id from the json dump of sellers.
        """
        response = self.client.search_business_seller('24103314000188')
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get('id'),
                         '27e17b778b404a83bf8e25ec995e2ffe')
        self.assertIsInstance(response.instance, BusinessSeller)
        self.assertEqual(response.instance.id,
                         '27e17b778b404a83bf8e25ec995e2ffe')

    @patch('ZoopAPIWrapper.wrapper.requests.post')
    def test_add_individual_seller(self, mocked_post):

        mocked_post.return_value = MagicMock(content='{}', status_code=201)

        data = {
            "taxpayer_id": gen.cpf(),
            'first_name': 'foo',
            'last_name': 'bar',
            'email': 'foo@bar.com',
            'phone_number': '+55 84 99999-9999',
            'birthdate': '1994-12-27',

            # 'address': {
            #     'line1': 'foo',
            #     'line2': '123',
            #     'line3': 'barbar',
            #     'neighborhood': 'fooofoo',
            #     'city': 'Natal',
            #     'state': 'BR-RN',
            #     'postal_code': '59152250',
            #     'country_code': "BR"
            # }
        }

        response = self.client.add_individual_seller(data)
        self.assertEqual(response.status_code, 201, msg=response.error)

    def test_add_individual_seller_duplicated(self):
        """
        the zoop api returns 409 if theres a unique attribute
        duplicated on the DB. Such as taxpayer_id.
        Got this taxpayer_id from sellers json dump.
        """
        data = {
            "taxpayer_id": 12685293892,
            'first_name': 'foo',
            'last_name': 'bar',
            'email': 'foo@bar.com',
            'phone_number': '+55 84 99999-9999',
            'birthdate': '1994-12-27',

            # 'address': {
            #     'line1': 'foo',
            #     'line2': '123',
            #     'line3': 'barbar',
            #     'neighborhood': 'fooofoo',
            #     'city': 'Natal',
            #     'state': 'BR-RN',
            #     'postal_code': '59152250',
            #     'country_code': "BR"
            # }
        }

        response = self.client.add_individual_seller(data)
        self.assertEqual(response.status_code, 409, msg=response.data)

    @patch('ZoopAPIWrapper.wrapper.requests.delete')
    def test_remove_seller(self, mocked_delete):
        """
        Test remove_seller method.
        Got the seller id from sellers dump.

        Args:
            mocked_delete: mock of object 'delete' from 'requests'
                            on file 'ZoopAPIWrapper.api'
        """
        mocked_delete.return_value = MagicMock(content='{}', status_code=200)

        response = self.client.remove_seller('0b6dbebcb5f24473ac730537e873b4d8')
        self.assertEqual(response.status_code, 200, msg=response.data)

        mocked_delete.assert_called_once_with(
            f'https://api.zoop.ws/v1/marketplaces/{MARKETPLACE_ID}/'
            f'sellers/0b6dbebcb5f24473ac730537e873b4d8/', auth=(ZOOP_KEY, ''))

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

    def test_list_seller_bank_accounts(self):
        """
        Test list_seller_bank_accounts method.
        Got this costumer (seller_id) from the json dump of bank_accounts.
        """
        response = self.client.list_seller_bank_accounts(
            'ee7e4b3683f8461a89e173dfb9d41d2c')
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get('items')
        self.assertTrue(items)

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

    # def test_get_bank_account(self):
    #     response_as_dict = self.zoop.get_bank_account(MAIN_SELLER)
    #     print(response_as_dict)
    #
    # def test_list_transactions(self):
    #     response_as_dict = self.zoop.list_transactions(MAIN_SELLER)
    #     print(response_as_dict)
