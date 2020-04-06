from tests.utils import SetTestCase
from ZoopAPIWrapper.models.transaction import Transaction


class TransactionTestCase(SetTestCase):
    def test_non_required_fields(self):
        self.assertIsSubSet(
            {"status", "confirmed", "original_amount", "transaction_number",
             "gateway_authorizer", "app_transaction_uid", "refunds", "rewards",
             "discounts", "pre_authorization", "sales_receipt",
             "statement_descriptor", "point_of_sale", "installment_plan",
             "refunded", "voided", "captured", "fees", "fee_details",
             "location_latitude", "location_longitude", "individual",
             "business", "expected_on", "history"},
            Transaction.get_non_required_fields()
        )

    def test_required_fields(self):
        self.assertEqual(
            {'amount', 'currency', 'description', 'reference_id',
             'on_behalf_of', 'customer', 'payment_type', 'payment_method'},
            Transaction.get_required_fields()
        )
