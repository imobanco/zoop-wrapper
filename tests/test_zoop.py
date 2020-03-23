import json
from unittest import TestCase
from unittest.mock import patch, MagicMock

from pycpfcnpj import gen

from ZoopAPIWrapper.api import Zoop, MAIN_SELLER, MARKETPLACE_ID, ZOOP_KEY
from ZoopAPIWrapper.models.seller import BusinessSeller, IndividualSeller
from ZoopAPIWrapper.models.bank_account import BankAccount


class ZoopTestCase(TestCase):
    def setUp(self):
        self.zoop = Zoop()

    def tearDown(self):
        del self.zoop

    def test_construct_url(self):
        action = 'teste'
        identifier = '123'

        url = self.zoop._Zoop__construct_url(action, identifier)

        self.assertEqual(url, f'https://api.zoop.ws/v1/marketplaces/'
                              f'{MARKETPLACE_ID}/teste/123/')

    def test_process_response(self):
        response = MagicMock(
            content='{"error": {"message": "foo"}}'
        )

        processed_response = self.zoop._Zoop__process_response(response)
        self.assertEqual(processed_response.data, {"error": {"message": "foo"}})
        self.assertEqual(processed_response.error, "foo")

    def test_process_response_resource(self):
        response = MagicMock(
            content='{"resource": "test"}'
        )

        processed_response = self.zoop._Zoop__process_response(response)
        self.assertIsNone(processed_response.instance)

    def test_process_response_resource_list(self):
        response = MagicMock(
            content='{"resource": "list", "items": '
                    '[{"resource": "test", "message": "foo"}]}'
        )

        processed_response = self.zoop._Zoop__process_response(response)
        self.assertEqual(len(processed_response.instances), 1)
        self.assertEqual(processed_response.instances, [None])

    def test_list_sellers(self):
        response = self.zoop.list_sellers()
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get('items')
        self.assertTrue(items)
        json_object = json.dumps(items, indent=4)
        with open("data/sellers.json", "w") as outfile:
            outfile.write(json_object)

    def test_retrieve_seller(self):
        response = self.zoop.retrieve_seller(MAIN_SELLER)
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get('id'),
                         '27e17b778b404a83bf8e25ec995e2ffe')
        self.assertIsInstance(response.instance, BusinessSeller)
        self.assertEqual(response.instance.id,
                         '27e17b778b404a83bf8e25ec995e2ffe')

    def test_search_seller_individual(self):
        response = self.zoop.search_individual_seller('12685293892')
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get('id'),
                         '29f1251bc7514b96ad5f6d873f9812a1')
        self.assertIsInstance(response.instance, IndividualSeller)
        self.assertEqual(response.instance.id,
                         '29f1251bc7514b96ad5f6d873f9812a1')

    def test_search_seller_business(self):
        response = self.zoop.search_business_seller('24103314000188')
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get('id'),
                         '27e17b778b404a83bf8e25ec995e2ffe')
        self.assertIsInstance(response.instance, BusinessSeller)
        self.assertEqual(response.instance.id,
                         '27e17b778b404a83bf8e25ec995e2ffe')

    @patch('ZoopAPIWrapper.api.requests.post')
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

        response = self.zoop.add_individual_seller(data)
        self.assertEqual(response.status_code, 201, msg=response.error)

    def test_add_individual_seller_duplicated(self):
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

        response = self.zoop.add_individual_seller(data)
        self.assertEqual(response.status_code, 409, msg=response.data)

    @patch('ZoopAPIWrapper.api.requests.delete')
    def test_remove_seller(self, mocked_delete):
        mocked_delete.return_value = MagicMock(content='{}', status_code=200)

        response = self.zoop.remove_seller('0b6dbebcb5f24473ac730537e873b4d8')
        self.assertEqual(response.status_code, 200, msg=response.data)

        mocked_delete.assert_called_once_with(
            f'https://api.zoop.ws/v1/marketplaces/{MARKETPLACE_ID}/'
            f'sellers/0b6dbebcb5f24473ac730537e873b4d8/', auth=(ZOOP_KEY, ''))

    def test_list_bank_accounts(self):
        response = self.zoop.list_bank_accounts()
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get('items')
        self.assertTrue(items)
        json_object = json.dumps(items, indent=4)
        with open("data/bank_accounts.json", "w") as outfile:
            outfile.write(json_object)

    def test_list_seller_bank_accounts(self):
        response = self.zoop.list_seller_bank_accounts(
            'ee7e4b3683f8461a89e173dfb9d41d2c')
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get('items')
        self.assertTrue(items)

    def test_retrieve_bank_account(self):
        response = self.zoop.retrieve_bank_account(
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
