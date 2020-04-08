from tests.utils import APITestCase
from zoop_wrapper.models.transaction import Transaction
from tests.factories.transaction import TransactionFactory


class TransactionWrapperMethodsTestCase(APITestCase):
    def test_list_transactions(self):
        """
        Test list_transactions method
        """
        self.set_get_mock(
            200,
            {
                'items': [TransactionFactory()]
            }
        )

        response = self.client.list_transactions()
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get('items')
        self.assertTrue(items)

    def test_list_transactions_for_seller(self):
        """
        Test list_transactions_for_seller method
        """
        self.set_get_mock(
            200,
            {
                'items': [TransactionFactory(on_behalf_of='foo')]
            }
        )

        response = self.client.list_transactions_for_seller('foo')
        self.assertEqual(response.status_code, 200, msg=response.data)
        items = response.data.get('items')
        self.assertTrue(items)

    def test_retrieve_transaction(self):
        """
        Test retrieve_transaction method.
        """
        self.set_get_mock(
            200,
            TransactionFactory(id='foo').to_dict()
        )

        response = self.client.retrieve_transaction('foo')
        self.assertEqual(response.status_code, 200, msg=response.data)
        self.assertEqual(response.data.get('id'), 'foo')
        self.assertIsInstance(response.instance, Transaction)
        self.assertEqual(response.instance.id, 'foo')

    def test_add_transaction(self):
        self.set_post_mock(
            201,
            TransactionFactory().to_dict()
        )

        data = {
            'amount': '1000',
            'currency': 'BRL',
            'description': 'meu boleto gerado para teste',
            'on_behalf_of': 'seller_id',
            'customer': 'buyer_id',
            'payment_type': 'boleto',
            'payment_method': {
                'expiration_date': '2020-06-20',
                'payment_limit_date': '2020-06-30',
                'billing_instructions': {
                    'late_fee': {
                        'mode': 'FIXED',
                        'percentage': 30,
                        'start_date': '2020-06-20'
                    },
                    'interest': {
                        'mode': 'MONTHLY_PERCENTAGE',
                        'percentage': 30,
                        'start_date': '2020-06-20'
                    },
                    'discount': [{
                        'mode': 'FIXED',
                        'amount': 300,
                        'limit_date': '2020-06-20'
                    }]
                }
            }
        }

        response = self.client.add_transaction(data)
        self.assertEqual(response.status_code, 201, msg=response.data)

    # def test_cancel_transaction(self):
    # @TODO: terminar cancel transaction
    #
    #     self.set_delete_mock(
    #         200,
    #         {
    #             'id': 'foo',
    #             'resource': 'buyer',
    #             'deleted': True
    #         }
    #     )
    #
    #     response = self.client.remove_buyer('foo')
    #     self.assertEqual(response.status_code, 200, msg=response.data)
