from unittest import TestCase
from unittest.mock import patch, MagicMock

from ZoopAPIWrapper.models.utils import (
    _get_model_class_from_resource, get_instance_from_data)
from ZoopAPIWrapper.models.seller import Seller
from ZoopAPIWrapper.models.bank_account import BankAccount
from ZoopAPIWrapper.models.utils import Token


class UtilsTestCase(TestCase):
    def test_get_model(self):
        model_class = _get_model_class_from_resource('seller')
        self.assertEqual(model_class, Seller)

        model_class = _get_model_class_from_resource('bank_account')
        self.assertEqual(model_class, BankAccount)

        model_class = _get_model_class_from_resource('token')
        self.assertEqual(model_class, Token)

        self.assertRaises(ValueError, _get_model_class_from_resource, 'test')

    @patch('ZoopAPIWrapper.models.utils.Seller.from_dict')
    def test_get_instance_seller(self, mocked_from_dict):
        data = {'resource': 'seller'}

        get_instance_from_data(data)

        self.assertIsInstance(mocked_from_dict, MagicMock)
        mocked_from_dict.assert_called_once_with(data)

    @patch('ZoopAPIWrapper.models.utils.BankAccount.from_dict')
    def test_get_instance_bank_account(self, mocked_from_dict):
        data = {'resource': 'bank_account'}

        get_instance_from_data(data)

        self.assertIsInstance(mocked_from_dict, MagicMock)
        mocked_from_dict.assert_called_once_with(data)

    @patch('ZoopAPIWrapper.models.utils.Token.from_dict')
    def test_get_instance_token(self, mocked_from_dict):
        data = {'resource': 'token'}

        get_instance_from_data(data)

        self.assertIsInstance(mocked_from_dict, MagicMock)
        mocked_from_dict.assert_called_once_with(data)
