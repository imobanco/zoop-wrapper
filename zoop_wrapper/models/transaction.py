from .base import ZoopObject, ResourceModel
from .card import Card
from .invoice import Invoice


class PointOfSale(ZoopObject):
    """
    Represents something (?)

    Attributes:
        entry_mode: ??
        identification_number: ??
    """

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union({"entry_mode", "identification_number"})


class History(ZoopObject):
    """
    Represents a update for :class:`.Transaction`

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
        fields = super().get_non_required_fields()
        return fields.union(
            {
                "id",
                "transaction",
                "amount",
                "operation_type",
                "status",
                "response_code",
                "response_message",
                "authorization_code",
                "authorizer_id",
                "authorization_nsu",
                "gatewayResponseTime",
                "authorizer",
                "created_at",
            }
        )


class Transaction(ResourceModel):
    """
    Represents a transaction
    https://docs.zoop.co/reference#transa%C3%A7%C3%A3o

    The :attr:`RESOURCE` is used to identify this Model.
    Used to check against :attr:`.resource`!

    Attributes:
        amount (int): integer amount value in 'centavos'
        currency (str): coin currency string
        description (str): value description
        reference_id: ??
        on_behalf_of (str): seller uuid identifier
        customer (str): customer uuid identifier
        status (str): value for status
        confirmed (str): value of cofirmation
        original_amount (int): original amount value
        transaction_number: ??
        gateway_authorizer: ??
        app_transaction_uid: ??
        refunds: ??
        rewards: ??
        discounts: ??
        pre_authorization: ??
        sales_receipt:
        statement_descriptor (str): value description
        installment_plan: ??
        refunded (bool): boolean of verification
        voided (bool): boolean of verification
        captured (bool): boolean of verification
        fees: ??
        fee_details: ??
        location_latitude: ??
        location_longitude: ??
        individual: ??
        business: ??
        expected_on (str):datetime string

        payment_type (str): payment type
        payment_method (:class:`.Card` or :class:`.Invoice`): payment method used
        point_of_sale (:class:`.PointOfSale`): ??
        history (list of :class:`.History`): transaction updates

    """

    RESOURCE = "transaction"

    CREDIT_TYPE = "credit"
    BOLETO_TYPE = "boleto"

    PAYMENT_TYPES = {CREDIT_TYPE, BOLETO_TYPE}

    def init_custom_fields(
        self,
        payment_type=None,
        payment_method=None,
        point_of_sale=None,
        history=None,
        currency="BRL",
        **kwargs,
    ):
        """
        Initialize :attr:`payment_method` as :class:`.Card` or :class:`.Invoice`
        based on data.

        Initialize :attr:`point_of_sale` as :class:`.PointOfSale`.

        Initialize :attr:`history` as list of :class:`.History`.

        Args:
            payment_type (str): value for payment type
            payment_method (dict or :class:`.Card` or :class:`.Invoice`): payment method data
            point_of_sale (dict or :class:`.PointOfSale`): point of sale data
            history (dict or :class:`.History` or list of either): history data. May be a list of dict or list of :class:`.History`
            currency (str): default currency is 'BRL'.
                So users may not need to pass currency!
            **kwargs: kwargs
        """
        setattr(self, "currency", currency)

        if payment_type not in Transaction.PAYMENT_TYPES:
            raise ValueError(
                f"payment_type must be one " f"of {Transaction.PAYMENT_TYPES}"
            )
        elif payment_type == Transaction.CREDIT_TYPE:
            setattr(
                self,
                "payment_method",
                Card.from_dict_or_instance(
                    payment_method, allow_empty=self._allow_empty
                ),
            )
        else:
            setattr(
                self,
                "payment_method",
                Invoice.from_dict_or_instance(
                    payment_method, allow_empty=self._allow_empty
                ),
            )

        setattr(
            self,
            "point_of_sale",
            PointOfSale.from_dict_or_instance(point_of_sale, allow_empty=True),
        )

        if isinstance(history, list):
            setattr(
                self,
                "history",
                [
                    History.from_dict_or_instance(item, allow_empty=True)
                    for item in history
                ],
            )
        else:
            setattr(
                self,
                "history",
                [History.from_dict_or_instance(history, allow_empty=True)],
            )

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union(
            {
                "amount",
                "currency",
                "description",
                "on_behalf_of",
                "customer",
                "payment_type",
                "payment_method",
            }
        )

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {
                "status",
                "confirmed",
                "original_amount",
                "transaction_number",
                "gateway_authorizer",
                "app_transaction_uid",
                "refunds",
                "rewards",
                "discounts",
                "pre_authorization",
                "sales_receipt",
                "reference_id",
                "statement_descriptor",
                "point_of_sale",
                "installment_plan",
                "refunded",
                "voided",
                "captured",
                "fees",
                "fee_details",
                "location_latitude",
                "location_longitude",
                "individual",
                "business",
                "expected_on",
                "history",
            }
        )


class Source(ZoopObject):

    CARD_PRESENT_TYPE = "card_present_type"
    CARD_NOT_PRESENT_TYPE = "card_not_present_type"

    SOURCE_TYPES = {CARD_PRESENT_TYPE, CARD_NOT_PRESENT_TYPE}

    def init_custom_fields(
        self,
        source_type=None,
        card=None,
        **kwargs,
    ):
        if source_type not in Source.SOURCE_TYPES:
            raise ValueError(
                f"O parâmetro source_type deve ser um " f"de {Source.SOURCE_TYPES}"
            )
        elif source_type == Source.CARD_PRESENT_TYPE:
            setattr(self, "card", card)
        else:
            if card.id is None:
                raise ValueError(
                    "É obrigatório que se forneça o id do cartão. O cartão passado possui."
                )
            else:
                setattr(self, "card",
                        Card.from_dict_or_instance(card, allow_empty=True))

    def get_validation_fields(self):
        """
        Get ``validation fields`` for instance.\n

        if :attr:`token_type` is :attr:`CARD_TYPE` card return
        :meth:`get_card_required_fields`.

        else :attr:`token_type` is :attr:`BANK_ACCOUNT_TYPE`!
        ``fields`` is :meth:`get_bank_account_required_fields`.\n
        if ``bank account type`` is :attr:`.INDIVIDUAL_TYPE` return ``fields`` union
        :meth:`.get_individual_required_fields`.\n

        else ``bank account type`` is :attr:`.BUSINESS_TYPE` return ``fields`` union
        :meth:`.get_business_required_fields`.

        Returns:
            ``set`` of fields to be validated
        """
        fields = set()

        if self.token_type == self.CARD_TYPE:
            return fields.union(self.get_card_required_fields())
        else:
            fields = fields.union(self.get_bank_account_required_fields())
            if self.get_bank_account_type() == BankAccount.INDIVIDUAL_TYPE:
                return fields.union(BankAccount.get_individual_required_fields())
            else:
                return fields.union(BankAccount.get_business_required_fields())

    def get_all_fields(self):
        """
        Get ``all fields`` for instance.

        ``fields`` is :meth:`get_validation_fields`

        if :attr:`token_type` is :attr:`CARD_TYPE` return
        ``fields`` union :meth:`get_card_non_required_fields`.

        else :attr:`token_type` is :attr:`BANK_ACCOUNT_TYPE` return
        ``fields`` union :meth:`get_bank_account_non_required_fields`.

        Returns:
            ``set`` of all fields
        """
        fields = self.get_validation_fields()

        if self.token_type == self.CARD_TYPE:
            return fields.union(self.get_card_non_required_fields())
        else:
            return fields.union(self.get_bank_account_non_required_fields())

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union(
            {
                "card",
                "type",
            }
        )

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {
                "amount",
                "currency",
                "usage",
            }
        )
