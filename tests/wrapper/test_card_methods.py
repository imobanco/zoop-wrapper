from unittest.mock import patch, MagicMock

from requests import HTTPError

from ..utils import APITestCase
from ..factories.buyer import BuyerFactory
from ..factories.card import CardFactory
from ..factories.seller import SellerFactory
from ..factories.token import CardTokenFactory, CreateCardTokenFactory
from zoop_wrapper.exceptions import ValidationError


class ZoopWrapperCardMethodsTestCase(APITestCase):
    def test_retrieve_card(self):
        """
        Test retrieve_card method.
        """
        self.set_get_mock(200, CardFactory(id="foo").to_dict())

        response = self.client.list_bank_accounts_by_seller("foo")
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get("id"), "foo")

    def test_add_card_token(self):
        """
        Test __add_card_token method.
        """
        self.set_post_mock(201, CardTokenFactory(allow_empty=True).to_dict())

        instance = CreateCardTokenFactory()

        response = self.client._CardWrapper__add_card_token(instance)
        self.assertEqual(response.status_code, 201, msg=response.data)

    @patch("zoop_wrapper.wrapper.ZoopWrapper._CardWrapper__add_card_token")
    def test_add_card(self, mocked_add_token):
        """
        Testa o método add_card. No cenário em que é passado um buyer
        """
        mocked_add_token.return_value = MagicMock(
            instance=CardTokenFactory(allow_empty=True)
        )

        self.set_post_mock(200, CardFactory(id="foo").to_dict())

        self.set_get_mock(200, BuyerFactory(id="bar").to_dict())

        data = CreateCardTokenFactory().to_dict()

        response = self.client.add_card(data, "bar")
        self.assertEqual(response.status_code, 200, msg=response.data)

    @patch("zoop_wrapper.wrapper.ZoopWrapper._CardWrapper__add_card_token")
    def test_add_card_buyer(self, mocked_add_token):
        """
        Testa se o método add_card está chamando o retrieve_buyer corretamente
        """

        data = CreateCardTokenFactory().to_dict()

        with patch(
            "zoop_wrapper.wrapper.BuyerWrapper.retrieve_buyer"
        ) as mocked_retrieve:
            self.client.add_card(data, "bar")

            self.assertIsInstance(mocked_retrieve, MagicMock)
            mocked_retrieve.assert_called_once_with("bar")

    @patch("zoop_wrapper.wrapper.ZoopWrapper._CardWrapper__add_card_token")
    def test_add_card_seller(self, mocked_add_token):
        """
        Testa se o método add_card está chamando o retrieve_seller corretamente
        """

        def request_get(url, **kwargs):
            if "buyer" in url:
                raise HTTPError()
            return self.build_response_mock(200, SellerFactory(id="bar").to_dict())

        self.mocked_get.side_effect = request_get

        data = CreateCardTokenFactory().to_dict()

        with patch(
            "zoop_wrapper.wrapper.SellerWrapper.retrieve_seller"
        ) as mocked_retrieve:
            self.client.add_card(data, "bar")

            self.assertIsInstance(mocked_retrieve, MagicMock)
            mocked_retrieve.assert_called_once_with("bar")

    @patch("zoop_wrapper.wrapper.ZoopWrapper._CardWrapper__add_card_token")
    def test_add_card_raise_validation_error(self, mocked_add_token):
        """
        Testa se o método add_card irá levantar a exceção corretamente
        """

        def request_get(url, **kwargs):
            raise HTTPError()

        self.mocked_get.side_effect = request_get

        data = CreateCardTokenFactory().to_dict()

        with self.assertRaises(ValidationError):
            self.client.add_card(data, "bar")
