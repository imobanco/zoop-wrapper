from tests.utils import SetTestCase
from zoop_wrapper.models.transaction import History


class HistoryTestCase(SetTestCase):
    def test_non_required_fields(self):
        self.assertEqual(
            {
                "amount",
                "authorization_code",
                "authorization_nsu",
                "authorizer",
                "authorizer_id",
                "created_at",
                "gatewayResponseTime",
                "id",
                "operation_type",
                "response_code",
                "response_message",
                "status",
                "transaction",
            },
            History.get_non_required_fields(),
        )
