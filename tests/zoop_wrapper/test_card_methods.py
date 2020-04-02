from unittest.mock import patch, MagicMock

from tests.utils import RequestsMockedTestCase
from ZoopAPIWrapper.wrapper import ZoopWrapper
from ZoopAPIWrapper.models.card import Card
from ZoopAPIWrapper.models.factories.card import (
    CardFactory)
from ZoopAPIWrapper.models.factories.token import TokenFactory
from ZoopAPIWrapper.models.factories.seller import IndividualSellerFactory


class ZoopWrapperCardMethodsTestCase(RequestsMockedTestCase):
    def setUp(self):
        super().setUp()
        self.client = ZoopWrapper()

    def tearDown(self):
        del self.client

    def test_retrieve_card(self):
        """
        Test retrieve_card method.
        """
        self.set_get_mock(
            200,
            CardFactory(
                id='foo'
            ).to_dict()
        )

        response = self.client.list_bank_accounts()
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get('id'), 'foo')
        self.assertIsInstance(response.instance, Card)
        self.assertEqual(response.instance.id, 'foo')

    # def test_add_card_token(self):
    #     """
    #     Test __add_card_token method.
    #     """
    #     self.set_post_mock(
    #         201,
    #         TokenFactory(
    #             type='card'
    #         ).to_dict()
    #     )
    #
    #     card = CardFactory()
    #
    #     response = self.client.\
    #         _ZoopWrapper__add_card_token(card)
    #     self.assertEqual(response.status_code, 201, msg=response.data)
    #
    # @patch('ZoopAPIWrapper.wrapper.ZoopWrapper._ZoopWrapper__add_card_token')
    # def test_add_card(self, mocked_add_token):
    #     """
    #     Test add_card method.
    #     """
    #     mocked_add_token.return_value = MagicMock(
    #         instance=TokenFactory(
    #             type='card'
    #         )
    #     )
    #
    #     data = CardFactory(
    #         id='foo',
    #         customer='bar'
    #     ).to_dict()
    #
    #     self.set_post_mock(
    #         200,
    #         data
    #     )
    #
    #     self.set_get_mock(
    #         200,
    #         IndividualSellerFactory(
    #             id='bar'
    #         ).to_dict()
    #     )
    #
    #     response = self.client.add_card(data)
    #     self.assertEqual(response.status_code, 200, msg=response.data)
    #     self.assertEqual(data.get('id'), 'foo', msg=data)
    #     self.assertIsInstance(response.instance, Card)
    #     self.assertEqual(response.instance.id, 'foo')
