from unittest.mock import patch, MagicMock

from tests.utils import APITestCase
from zoop_wrapper.models.card import Card
from tests.factories.buyer import BuyerFactory
from tests.factories.card import CardFactory
from tests.factories.token import CardTokenFactory, CreateCardTokenFactory


class ZoopWrapperCardMethodsTestCase(APITestCase):
    def test_retrieve_card(self):
        """
        Test retrieve_card method.
        """
        self.set_get_mock(200, CardFactory(id="foo").to_dict())

        response = self.client.list_bank_accounts()
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get("id"), "foo")
        self.assertIsInstance(response.instance, Card)
        self.assertEqual(response.instance.id, "foo")

    def test_add_card_token(self):
        """
        Test __add_card_token method.
        """
        self.set_post_mock(201, CardTokenFactory(allow_empty=True).to_dict())

        instance = CreateCardTokenFactory()

        response = self.client._ZoopWrapper__add_card_token(instance)
        self.assertEqual(response.status_code, 201, msg=response.data)

    @patch("zoop_wrapper.wrapper.ZoopWrapper._ZoopWrapper__add_card_token")
    def test_add_card(self, mocked_add_token):
        """
        Test add_card method.
        """
        mocked_add_token.return_value = MagicMock(
            instance=CardTokenFactory(allow_empty=True)
        )

        self.set_post_mock(200, CardFactory(id="foo").to_dict())

        self.set_get_mock(200, BuyerFactory(id="bar").to_dict())

        data = CreateCardTokenFactory().to_dict()

        response = self.client.add_card(data, "bar")
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertIsInstance(response.instance, Card)
        self.assertEqual(response.instance.id, "foo")
