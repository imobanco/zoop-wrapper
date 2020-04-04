from ZoopAPIWrapper.models.base import (
    ZoopObject, ResourceModel)


class PointOfSale(ZoopObject):
    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {'entry_mode', 'identification_number'}
        )


class History(ZoopObject):
    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {"id", "transaction", "amount", "operation_type",
             "status", "response_code", "response_message",
             "authorization_code", "authorizer_id", "authorization_nsu",
             "gatewayResponseTime", "authorizer", "created_at"}
        )


# class HistoryList(ZoopObject):
#     pass


class Transaction(ResourceModel):
    """

    """
    RESOURCE = 'transaction'

    FIELDS = {
        "status", "confirmed", "amount", "original_amount",
        "currency", "description", "payment_type", "transaction_number",
        "gateway_authorizer", "app_transaction_uid", "refunds",
        "rewards", "discounts", "pre_authorization", "sales_receipt",
        "on_behalf_of", "customer", "statement_descriptor", "payment_method",
        "point_of_sale", "installment_plan", "refunded", "voided",
        "captured", "fees", "fee_details", "location_latitude",
        "location_longitude", "individual", "business", "expected_on",
        "history"
    }

