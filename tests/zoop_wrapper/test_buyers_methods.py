import json
from unittest import TestCase
from unittest.mock import patch, MagicMock

from pycpfcnpj import gen

from ZoopAPIWrapper.wrapper import ZoopWrapper
from ZoopAPIWrapper.models.buyer import Buyer


class ZoopWrapperBuyerMethodsTestCase(TestCase):
    def setUp(self):
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
        pass

    def test_remove_buyer(self):
        pass

