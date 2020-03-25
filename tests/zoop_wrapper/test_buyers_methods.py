import json

from pycpfcnpj import gen

from tests.utils import MockedPostDeleteTestCase
from ZoopAPIWrapper.wrapper import ZoopWrapper
from ZoopAPIWrapper.models.buyer import Buyer


class ZoopWrapperBuyerMethodsTestCase(MockedPostDeleteTestCase):
    def setUp(self):
        super().setUp()
        self.client = ZoopWrapper()

    def tearDown(self):
        del self.client

    def test_list_buyers(self):
        """
        Test list_buyers method.
        And create a dump with all buyers.
        """

        response = self.client.list_buyers()
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get('items')
        self.assertTrue(items)
        json_object = json.dumps(items, indent=4)
        with open("data/buyers.json", "w") as outfile:
            outfile.write(json_object)

    def test_retrieve_buyer(self):
        """
        Test retrieve_buyer method.
        Got this buyer id from the json dump of buyers.
        """
        response = self.client.retrieve_buyer(
            '093bad87c86649528e0286388a325867')
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get('id'),
                         '093bad87c86649528e0286388a325867')
        self.assertIsInstance(response.instance, Buyer)
        self.assertEqual(response.instance.id,
                         '093bad87c86649528e0286388a325867')

    def test_search_buyer(self):
        """
        Test search_buyer method.
        Got this buyer identifier from the json dump of buyers.
        """
        response = self.client.search_buyer(
            '13398287409')
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get('id'),
                         'd8a5299cc72b4971b42845ed68cbf75c')
        self.assertIsInstance(response.instance, Buyer)
        self.assertEqual(response.instance.id,
                         'd8a5299cc72b4971b42845ed68cbf75c')

    def test_add_buyer(self):
        self.set_post_mock(
            201,
            {"id": "bf589dd424e64cc49348bf3192bc0db5", "status": "active",
             "resource": "buyer", "account_balance": "0.00",
             "current_balance": "0.00", "first_name": "foo",
             "last_name": "foo", "taxpayer_id": "23859566083",
             "description": None, "email": "foo@bar.com",
             "phone_number": "foo", "facebook": None, "twitter": None,
             "address": {"line1": None, "line2": None, "line3": None,
                         "neighborhood": None, "city": None, "state": None,
                         "postal_code": None, "country_code": None},
             "delinquent": False, "payment_methods": None,
             "default_debit": None, "default_credit": None,
             "default_receipt_delivery_method": None,
             "uri": "/v1/marketplaces/d77c2258b51d49269191502695f939f4/buyers"
                    "/bf589dd424e64cc49348bf3192bc0db5", "metadata": {},
             "created_at": "2020-03-25T20:53:13+00:00",
             "updated_at": "2020-03-25T20:53:13+00:00"})

        data = {
            "first_name": "foo",
            "last_name": "foo",
            "email": 'foo@bar.com',
            "taxpayer_id": gen.cpf(),
            "phone_number": "foo",
            "birthdate": 'foo',
            "address": {
                "line1": "foo",
                "line2": "foo",
                "line3": "foo",
                # "neighborhood": "foo",
                "city": "foo",
                "state": "RN",
                "postal_code": "foo",
                "country_code": "BR"
            }
        }

        response = self.client.add_buyer(data)
        self.assertEqual(response.status_code, 201, msg=response.data)

    def test_remove_buyer(self):
        self.set_delete_mock(
            200, {'id': 'a12c6bf830854b5d9c1d2d36cb1478a0',
                  'resource': 'buyer', 'deleted': True})

        response = self.client.remove_buyer('a12c6bf830854b5d9c1d2d36cb1478a0')
        self.assertEqual(response.status_code, 200, msg=response.data)
