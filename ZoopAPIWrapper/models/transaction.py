from ZoopAPIWrapper.models.base import (
    ZoopObject, ResourceModel)
from ZoopAPIWrapper.models.card import Card
from ZoopAPIWrapper.models.invoice import Invoice


class PointOfSale(ZoopObject):
    """
    Represents something (?)

    Attributes:
        entry_mode: ??
        identification_number: ??
    """
    @classmethod
    def get_non_required_fields(cls):
        """
        get set of non required fields

        Returns: set of fields
        """
        fields = super().get_non_required_fields()
        return fields.union(
            {'entry_mode', 'identification_number'}
        )


class History(ZoopObject):
    """
    Represents a update for Transaction

    Attributes:
        id: uuid identifier
        transaction: transaction uuid identifier
        amount: amount value for the update
        operation_type: type for the update
        status: status for the update
        response_code: ??
        response_message: ??
        authorization_code: ??
        authorizer_id: ??
        authorization_nsu: ??
        gatewayResponseTime: ??
        authorizer: ??
        created_at: datetime for the update
    """
    @classmethod
    def get_non_required_fields(cls):
        """
        get set of non required fields

        Returns: set of fields
        """
        fields = super().get_non_required_fields()
        return fields.union(
            {"id", "transaction", "amount", "operation_type",
             "status", "response_code", "response_message",
             "authorization_code", "authorizer_id", "authorization_nsu",
             "gatewayResponseTime", "authorizer", "created_at"}
        )


class Transaction(ResourceModel):
    """
    Represents a transaction
    https://docs.zoop.co/reference#transa%C3%A7%C3%A3o

    Attributes:
        RESOURCE: resource model string

        CREDIT_TYPE: string for credit card type
        BOLETO_TYPE: string for boleto type (Invoice)

        PAYMENT_TYPES: a set with credit and boleto types

        amount: amount value
        currency: coin currency string
        description: string description
        reference_id: ??
        on_behalf_of: seller uuid identifier
        customer: customer uuid identifier
        status: string for status
        confirmed: string of cofirmation
        original_amount: original amount value
        transaction_number: ??
        gateway_authorizer: ??
        app_transaction_uid: ??
        refunds: ??
        rewards: ??
        discounts: ??
        pre_authorization: ??
        sales_receipt:
        statement_descriptor: string description
        installment_plan: ??
        refunded: boolean of verification
        voided: boolean of verification
        captured: boolean of verification
        fees: ??
        fee_details: ??
        location_latitude: ??
        location_longitude: ??
        individual: ??
        business: ??
        expected_on:datetime string

        payment_type: payment type string ('credit' or 'boleto')
        payment_method: Card instance or Invoice instance
        point_of_sale: PointOfSale instance
        history: List of History instance

    """
    RESOURCE = 'transaction'

    CREDIT_TYPE = 'credit'
    BOLETO_TYPE = 'boleto'

    PAYMENT_TYPES = {CREDIT_TYPE, BOLETO_TYPE}

    def init_custom_fields(self, payment_type=None, payment_method=None,
                           point_of_sale=None, history=None,
                           **kwargs):
        """
        Initialize payment_method based on payment_type from data.
        Initialize point_of_sale and history from data.

        Args:
            payment_type: string for payment type
            payment_method: dict of data or instance
            point_of_sale:  dict of data or instance of PointOfSale
            history:  dict of data or instance or list of History
            **kwargs: kwargs
        """
        if payment_type not in Transaction.PAYMENT_TYPES:
            raise ValueError(f'payment_type must be one of {Transaction.PAYMENT_TYPES}')
        elif payment_type == Transaction.CREDIT_TYPE:
            setattr(
                self, 'payment_method',
                Card.from_dict_or_instance(payment_method, allow_empty=self._allow_empty))
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
        """
        get set of required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {'amount', 'currency', 'description', 'reference_id',
             'on_behalf_of', 'customer', 'payment_type', 'payment_method'}
        )

    @classmethod
    def get_non_required_fields(cls):
        """
        get set of non required fields

        Returns: set of fields
        """
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
