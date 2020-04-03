from pycpfcnpj import gen

from tests.utils import APITestCase
from ZoopAPIWrapper.models.buyer import Buyer
from tests.factories.buyer import BuyerFactory


class ZoopWrapperBuyerMethodsTestCase(APITestCase):
    def test_list_buyers(self):
        """
        Test list_buyers method
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
            BuyerFactory(id='foo').to_dict()
        )

        response = self.client.retrieve_buyer('foo')
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get('id'), 'foo')
        self.assertIsInstance(response.instance, Buyer)
        self.assertEqual(response.instance.id, 'foo')

    def test_search_buyer(self):
        """
        Test search_buyer method.
        Got this buyer identifier from the json dump of buyers.
        """
        self.set_get_mock(
            200,
            BuyerFactory(
                id='foo',
                taxpayer_id='bar'
            ).to_dict()
        )

        response = self.client.search_buyer('bar')
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get('id'), 'foo')
        self.assertIsInstance(response.instance, Buyer)
        self.assertEqual(response.instance.id, 'foo')

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
        """
        the zoop api returns 200 and this content on delete request
        """
        self.set_delete_mock(
            200,
            {
                'id': 'foo',
                'resource': 'buyer',
                'deleted': True
            }
        )

        response = self.client.remove_buyer('foo')
        self.assertEqual(response.status_code, 200, msg=response.data)
