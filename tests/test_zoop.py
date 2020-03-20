import json
from unittest import TestCase
from unittest.mock import patch, MagicMock

from pycpfcnpj import gen

from ZoopAPIWrapper.zoop import Zoop, MAIN_SELLER


class TestZoop(TestCase):
    def setUp(self):
        self.zoop = Zoop()

    def tearDown(self):
        del self.zoop

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
        self.assertEqual(response.data.get('id'), '27e17b778b404a83bf8e25ec995e2ffe')

    @patch('ZoopAPIWrapper.zoop.requests.post')
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
            "taxpayer_id": 59432919110,
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
        self.assertEqual(response.status_code, 409, msg=response.error)


    # def test_get_bank_account(self):
    #     response_as_dict = self.zoop.get_bank_account(MAIN_SELLER)
    #     print(response_as_dict)
    #
    # def test_list_transactions(self):
    #     response_as_dict = self.zoop.list_transactions(MAIN_SELLER)
    #     print(response_as_dict)


if __name__ == '__main__':
    unittest.main()
