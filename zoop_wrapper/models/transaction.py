from .base import ZoopObject, ResourceModel
from .card import Card
from .invoice import Invoice
from .token import Token
from ..exceptions import ValidationError


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

    CARD_TYPE = "credit"
    BOLETO_TYPE = "boleto"

    PAYMENT_TYPES = {CARD_TYPE, BOLETO_TYPE}

    def init_custom_fields(
        self,
        payment_type=None,
        payment_method=None,
        source=None,
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
        elif payment_type == Transaction.CARD_TYPE:
            setattr(
                self,
                "source",
                Source.from_dict_or_instance(source, allow_empty=self._allow_empty),
            )
        else:
            setattr(
                self,
                "payment_method",
                Invoice.from_dict_or_instance(
                    payment_method, allow_empty=self._allow_empty
                ),
            )

        setattr(self, "payment_type", payment_type)

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

        if self.payment_type == self.CARD_TYPE:
            return fields.union(self.get_card_required_fields())
        else:
            return fields.union(self.get_boleto_required_fields())

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

        return fields.union(self.get_non_required_fields())

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
            }
        )

    @classmethod
    def get_card_required_fields(cls):
        fields = cls.get_required_fields()
        return fields.union({"source",})

    @classmethod
    def get_boleto_required_fields(cls):
        fields = cls.get_required_fields()
        return fields.union({"payment_method",})

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
        self, card=None, type="card", currency="BRL", **kwargs,
    ):
        setattr(self, "type", type)
        setattr(self, "currency", currency)

        """
        Ver documentação do :meth:`.from_dict_or_instance`.
        
        Precisamos pegar o atributo `id` para identificar o tipo.
        """

        token_for_card = Token.from_dict_or_instance(card, allow_empty=True)

        if token_for_card.id is not None:
            card_type = Source.CARD_NOT_PRESENT_TYPE
        else:
            try:
                token_for_card = Token.from_dict_or_instance(card)
                card_type = Source.CARD_PRESENT_TYPE
            except ValidationError as e:
                raise ValidationError(
                    self,
                    f"Tipo do source não identificado! "
                    f"Utilize um dos tipos {Source.SOURCE_TYPES}",
                ) from e

        setattr(self, "card", token_for_card)
        setattr(self, "card_type", card_type)

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

        if self.card_type == self.CARD_PRESENT_TYPE:
            return fields.union(self.get_card_present_required_fields())
        else:
            return fields.union(self.get_card_not_present_required_fields())

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
        return self.get_validation_fields()

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union({"card", "type", "currency", "usage", "amount"})

    @classmethod
    def get_card_not_present_required_fields(cls):
        """
        Get ``set`` of ``non required fields`` for :attr:`CARD_TYPE`.

        Returns:
            ``set`` of fields
        """
        return cls.get_required_fields()

    @classmethod
    def get_card_present_required_fields(cls):
        """
        Método get do ``set`` de ``non required fields`` para :attr:`CARD_TYPE`.

        Returns:
            ``set`` de campos
        """
        fields = cls.get_required_fields()
        return fields.union({"amount", "usage"})
