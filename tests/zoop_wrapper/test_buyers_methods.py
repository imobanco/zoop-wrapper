from pycpfcnpj import gen

from tests.utils import RequestsMockedTestCase
from ZoopAPIWrapper.wrapper import ZoopWrapper
from ZoopAPIWrapper.models.buyer import Buyer
from ZoopAPIWrapper.models.factories.buyer import BuyerFactory


class ZoopWrapperBuyerMethodsTestCase(RequestsMockedTestCase):
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
        self.set_get_mock(
            200,
            {
                'items': [BuyerFactory()]
            }
        )

        response = self.client.list_buyers()
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get('items')
        self.assertTrue(items)

    def test_retrieve_buyer(self):
        """
        Test retrieve_buyer method.
        Got this buyer id from the json dump of buyers.
        """
        self.set_get_mock(
            200,
            BuyerFactory(
                id='093bad87c86649528e0286388a325867'
            ).to_dict()
        )

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
        self.set_get_mock(
            200,
            BuyerFactory(
                id='d8a5299cc72b4971b42845ed68cbf75c',
                taxpayer_id='13398287409'
            ).to_dict()
        )

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
            BuyerFactory().to_dict()
        )

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
            200,
            {
                'id': 'a12c6bf830854b5d9c1d2d36cb1478a0',
                'resource': 'buyer',
                'deleted': True
            }
        )

        response = self.client.remove_buyer('a12c6bf830854b5d9c1d2d36cb1478a0')
        self.assertEqual(response.status_code, 200, msg=response.data)
