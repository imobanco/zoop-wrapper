from unittest import TestCase
from unittest.mock import patch, MagicMock

from zoop_wrapper.models.utils import (
    _get_model_class_from_resource, get_instance_from_data)
from zoop_wrapper.models.seller import Seller
from zoop_wrapper.models.bank_account import BankAccount
from zoop_wrapper.models.token import Token


class UtilsTestCase(TestCase):
    def test_get_model_seller(self):
        model_class = _get_model_class_from_resource('seller')
        self.assertEqual(model_class, Seller)

    def test_get_model_bank_account(self):
        model_class = _get_model_class_from_resource('bank_account')
        self.assertEqual(model_class, BankAccount)

    def test_get_model_token(self):
        model_class = _get_model_class_from_resource('token')
        self.assertEqual(model_class, Token)

    def test_get_model_not_found(self):
        self.assertRaises(ValueError, _get_model_class_from_resource, 'test')

    @patch('zoop_wrapper.models.utils.Seller.from_dict')
    def test_get_instance_seller(self, mocked_from_dict):
        data = {'resource': 'seller'}

        get_instance_from_data(data)

        self.assertIsInstance(mocked_from_dict, MagicMock)
        mocked_from_dict.assert_called_once_with(data, allow_empty=True)

    @patch('zoop_wrapper.models.utils.BankAccount.from_dict')
    def test_get_instance_bank_account(self, mocked_from_dict):
        data = {'resource': 'bank_account'}

        get_instance_from_data(data)

        self.assertIsInstance(mocked_from_dict, MagicMock)
        mocked_from_dict.assert_called_once_with(data, allow_empty=True)

    @patch('zoop_wrapper.models.utils.Token.from_dict')
    def test_get_instance_token(self, mocked_from_dict):
        data = {'resource': 'token'}

        get_instance_from_data(data)

        self.assertIsInstance(mocked_from_dict, MagicMock)
        mocked_from_dict.assert_called_once_with(data, allow_empty=True)
