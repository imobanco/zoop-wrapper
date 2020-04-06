from ZoopAPIWrapper.models.base import (
    ZoopObject, ResourceModel)
from ZoopAPIWrapper.models.invoice import Invoice


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


class Transaction(ResourceModel):
    """

    """
    RESOURCE = 'transaction'

    CREDIT_TYPE = 'credit'
    BOLETO_TYPE = 'boleto'

    PAYMENT_TYPES = {CREDIT_TYPE, BOLETO_TYPE}

    def init_custom_fields(self, payment_type=None, payment_method=None,
                           point_of_sale=None, history=None,
                           **kwargs):
        if payment_type not in Transaction.PAYMENT_TYPES:
            raise ValueError(f'payment_type must be one of {Transaction.PAYMENT_TYPES}')
        elif payment_type == Transaction.CREDIT_TYPE:
            setattr(self, 'payment_method', payment_method)
        else:
            setattr(
                self, 'payment_method',
                Invoice.from_dict_or_instance(payment_method, allow_empty=self._allow_empty))

        setattr(
            self, 'point_of_sale',
            PointOfSale.from_dict_or_instance(
                point_of_sale, allow_empty=True))

        if isinstance(history, list):
            setattr(
                self, 'history',
                [
                    History.from_dict_or_instance(item, allow_empty=True)
                    for item in history
                ])
        else:
            setattr(
                self, 'history',
                [History.from_dict_or_instance(history, allow_empty=True)]
            )

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union(
            {'amount', 'currency', 'description', 'reference_id',
             'on_behalf_of', 'customer', 'payment_type', 'payment_method'}
        )

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {"status", "confirmed", "original_amount", "transaction_number",
             "gateway_authorizer", "app_transaction_uid", "refunds", "rewards",
             "discounts", "pre_authorization", "sales_receipt",
             "statement_descriptor", "point_of_sale", "installment_plan",
             "refunded", "voided", "captured", "fees", "fee_details",
             "location_latitude", "location_longitude", "individual",
             "business", "expected_on", "history"}
        )
