from tests.utils import SetTestCase
from zoop_wrapper.models.transaction import History


class HistoryTestCase(SetTestCase):
    def test_non_required_fields(self):
        self.assertEqual(
            {"id", "transaction", "amount", "operation_type",
             "status", "response_code", "response_message",
             "authorization_code", "authorizer_id", "authorization_nsu",
             "gatewayResponseTime", "authorizer", "created_at"},
            History.get_non_required_fields()
        )
