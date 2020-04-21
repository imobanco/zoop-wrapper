from pycpfcnpj import gen
from requests import HTTPError

from tests.utils import APITestCase
from zoop_wrapper.wrapper import MARKETPLACE_ID, ZOOP_KEY
from zoop_wrapper.models.seller import Seller
from tests.factories.seller import BusinessSellerFactory, IndividualSellerFactory
from tests.factories.bank_account import IndividualBankAccountFactory


class ZoopWrapperSellerMethodsTestCase(APITestCase):
    def test_list_sellers(self):
        """
        Test list_sellers method.
        """
        self.set_get_mock(200, {"items": [IndividualSellerFactory()]})

        response = self.client.list_sellers()
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get("items")
        self.assertTrue(items)

    def test_retrieve_seller(self):
        """
        Test retrieve_seller method.
        """
        self.set_get_mock(200, IndividualSellerFactory(id="foo").to_dict())

        response = self.client.retrieve_seller("foo")
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get("id"), "foo")
        self.assertIsInstance(response.instance, Seller)
        self.assertEqual(response.instance.id, "foo")

    def test_search_individual_seller(self):
        """
        Test search_individual_seller method.
        """
        self.set_get_mock(
            200, IndividualSellerFactory(id="foo").to_dict()
        )

        response = self.client.search_individual_seller("bar")
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get("id"), "foo")
        self.assertIsInstance(response.instance, Seller)
        self.assertEqual(response.instance.id, "foo")

    def test_search_business_seller(self):
        """
        Test search_business_seller method.
        """
        self.set_get_mock(200, BusinessSellerFactory(id="foo").to_dict())

        response = self.client.search_business_seller("bar")
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get("id"), "foo")
        self.assertIsInstance(response.instance, Seller)
        self.assertEqual(response.instance.id, "foo")

    def test_add_individual_seller(self):
        self.set_post_mock(201, {})

        data = {
            "taxpayer_id": gen.cpf(),
            "first_name": "foo",
            "last_name": "bar",
            "email": "foo@bar.com",
            "phone_number": "+55 84 99999-9999",
            "birthdate": "1994-12-27",
            "address": {
                "line1": "foo",
                "line2": "123",
                "line3": "barbar",
                "neighborhood": "fooofoo",
                "city": "Natal",
                "state": "BR-RN",
                "postal_code": "59152250",
                "country_code": "BR",
            },
        }

        response = self.client.add_seller(data)
        self.assertEqual(response.status_code, 201, msg=response.error)

    def test_add_individual_seller_duplicated(self):
        """
        the zoop api returns 409 if theres a unique attribute
        duplicated on the DB. Such as taxpayer_id.
        """
        self.set_post_mock(409, {"error": {"message": "Esse seller é duplicado!!!!"}})

        data = {
            "taxpayer_id": 12685293892,
            "first_name": "foo",
            "last_name": "bar",
            "email": "foo@bar.com",
            "phone_number": "+55 84 99999-9999",
            "birthdate": "1994-12-27",
            "address": {
                "line1": "foo",
                "line2": "123",
                "line3": "barbar",
                "neighborhood": "fooofoo",
                "city": "Natal",
                "state": "BR-RN",
                "postal_code": "59152250",
                "country_code": "BR",
            },
        }

        self.assertRaises(HTTPError, self.client.add_seller, data)

    def test_remove_seller(self):
        self.set_delete_mock(200, {"id": "foo", "resource": "seller", "deleted": True})

        response = self.client.remove_seller("foo")
        self.assertEqual(response.status_code, 200, msg=response.data)

        self.mocked_delete.assert_called_once_with(
            f"https://api.zoop.ws/v1/marketplaces/{MARKETPLACE_ID}/" f"sellers/foo/",
            auth=(ZOOP_KEY, ""),
        )

    def test_list_seller_bank_accounts(self):
        """
        Test list_seller_bank_accounts method
        """
        self.set_get_mock(
            200, {"items": [IndividualBankAccountFactory(customer="foo")]}
        )
        response = self.client.list_seller_bank_accounts("foo")
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get("items")
        self.assertTrue(items)
