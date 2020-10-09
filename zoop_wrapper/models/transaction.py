from .base import ZoopObject, ResourceModel
from .card import Card
from .invoice import Invoice
from .token import Token
from ..exceptions import ValidationError, FieldError

from zoop_wrapper.utils import convert_currency_float_value_to_cents


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
        amount: amount value for the update
        authorization_code: ??
        authorization_nsu: ??
        authorizer: ??
        authorizer_id: ??
        created_at: datetime for the update
        gatewayResponseTime: ??
        id: uuid identifier
        operation_type: type for the update
        response_code: ??
        response_message: ??
        status: status for the update
        transaction: transaction uuid identifier
    """

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
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
        app_transaction_uid: ??
        business: ??
        capture (bool): flag que designa se será uma transação simples {true} ou uma composta (com pre autorização) {false}  # noqa
        captured (bool): flag indica se a transação foi capturada ou não
        confirmed (str): value of cofirmation
        currency (str): coin currency string
        customer (str): customer uuid identifier
        description (str): value description
        discounts: ??
        expected_on (str):datetime string
        fee_details: ??
        fees: ??
        gateway_authorizer: ??
        history (list of :class:`.History`): transaction updates
        individual: ??
        installment_plan: ??
        location_latitude: ??
        location_longitude: ??
        on_behalf_of (str): seller uuid identifier
        original_amount (int): original amount value
        payment_method (:class:`.Card` or :class:`.Invoice`): payment method used
        payment_type (str): payment type
        point_of_sale (:class:`.PointOfSale`): ??
        pre_authorization: ??
        reference_id: ??
        refunded (bool): boolean of verification
        refunds: ??
        rewards: ??
        sales_receipt:
        statement_descriptor (str): value description
        status (str): value for status
        transaction_number: ??
        voided (bool): boolean of verification
    """

    RESOURCE = "transaction"

    CARD_TYPE = "credit"
    BOLETO_TYPE = "boleto"

    PAYMENT_TYPES = {CARD_TYPE, BOLETO_TYPE}

    def init_custom_fields(
        self,
        amount=None,
        currency="BRL",
        history=None,
        id=None,
        payment_method=None,
        payment_type=None,
        point_of_sale=None,
        source=None,
        **kwargs,
    ):
        """
        Initialize :attr:`payment_method` as :class:`.Card` or :class:`.Invoice`
        based on data.

        Initialize :attr:`point_of_sale` as :class:`.PointOfSale`.

        Initialize :attr:`history` as list of :class:`.History`.

        Args:
            currency (str): default currency is 'BRL'.
                So users may not need to pass currency!
            history (dict or :class:`.History` or list of either): history data. May be a list of dict or list of :class:`.History`  # noqa
            payment_method (dict or :class:`.Card` or :class:`.Invoice`): payment method data  # noqa
            payment_type (str): value for payment type
            point_of_sale (dict or :class:`.PointOfSale`): point of sale data
            **kwargs: kwargs
        """
        setattr(self, "currency", currency)

        if payment_type not in Transaction.PAYMENT_TYPES:
            raise ValidationError(
                self,
                f"payment_type precisa ser um valor "
                f"do conjunto {Transaction.PAYMENT_TYPES}",
            )

        if amount is not None:
            amount = convert_currency_float_value_to_cents(amount)
            setattr(self, "amount", amount)

        if id is not None and payment_type == Transaction.CARD_TYPE:
            setattr(
                self,
                "payment_method",
                Card.from_dict_or_instance(
                    payment_method, allow_empty=self._allow_empty
                ),
            )
        elif id is None and payment_type == Transaction.CARD_TYPE:
            setattr(
                self,
                "source",
                Source.from_dict_or_instance(source, allow_empty=self._allow_empty),
            )
        elif payment_type == Transaction.BOLETO_TYPE:
            setattr(
                self,
                "payment_method",
                Invoice.from_dict_or_instance(
                    payment_method, allow_empty=self._allow_empty
                ),
            )
        else:
            raise ValidationError(self, "Alguma coisa muito errada aconteceu!!")

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
        Pega os ``campos de validação`` para uma instância.\n

        O conjunto de campos é feito com base no :attr:`payment_type`.

        Se for :attr:`CARD_TYPE` utiliza o :meth:`get_card_required_fields`.

        Se não, ele é :attr:`payment_type` é :attr:`BOLETO_TYPE`!
        Utiliza o :meth:`get_boleto_required_fields`.

        Returns:
            ``set`` de campos para serem validados
        """
        fields = set()

        if self.payment_type == self.CARD_TYPE:
            return fields.union(self.get_card_required_fields())
        else:
            return fields.union(self.get_boleto_required_fields())

    def get_all_fields(self):
        """
        Pega ``todos os campos`` para instância.

        O conjunto de campos é construído com base no :meth:`get_validation_fields`
        com a união do :meth:`get_non_required_fields`.

        Returns:
            ``set`` de todos os campos
        """
        fields = self.get_validation_fields()

        return fields.union(self.get_non_required_fields())

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union(
            {"currency", "customer", "description", "on_behalf_of", "payment_type"}
        )

    @classmethod
    def get_card_required_fields(cls):
        fields = cls.get_required_fields()
        return fields.union({"source", "capture"})

    @classmethod
    def get_boleto_required_fields(cls):
        fields = cls.get_required_fields()
        return fields.union({"payment_method", "amount"})

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {
                "app_transaction_uid",
                "business",
                "captured",
                "confirmed",
                "discounts",
                "expected_on",
                "fee_details",
                "fees",
                "gateway_authorizer",
                "history",
                "individual",
                "installment_plan",
                "location_latitude",
                "location_longitude",
                "original_amount",
                "point_of_sale",
                "pre_authorization",
                "reference_id",
                "refunded",
                "refunds",
                "rewards",
                "sales_receipt",
                "statement_descriptor",
                "status",
                "transaction_number",
                "voided",
            }
        )


class Source(ZoopObject):

    CARD_PRESENT_TYPE = "card_present_type"
    CARD_NOT_PRESENT_TYPE = "card_not_present_type"

    SOURCE_TYPES = {CARD_PRESENT_TYPE, CARD_NOT_PRESENT_TYPE}

    def init_custom_fields(
        self,
        card=None,
        type="card",
        currency="BRL",
        installment_plan=None,
        **kwargs,
    ):
        setattr(self, "type", type)
        setattr(self, "currency", currency)

        kwargs["amount"] = convert_currency_float_value_to_cents(kwargs["amount"])

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

        if installment_plan:
            installment_plan = InstallmentPlan.from_dict_or_instance(installment_plan)

        setattr(self, "installment_plan", installment_plan)
        setattr(self, "card", token_for_card)
        setattr(self, "card_type", card_type)

    def get_validation_fields(self):
        """
        Pega ``campos de validação`` da instâcia.\n

        O conjunto de campos é construído com base no :attr:`card_type`.

        Se for :attr:`CARD_PRESENT_TYPE` utiliza o
        :meth:`get_card_present_required_fields`.

        Se não, utiliza o :meth:`get_card_not_present_required_fields`.

        Returns:
            ``set`` de campos para ser validados
        """
        fields = set()

        if self.card_type == self.CARD_PRESENT_TYPE:
            return fields.union(self.get_card_present_required_fields())
        else:
            return fields.union(self.get_card_not_present_required_fields())

    def get_all_fields(self):
        """
        Pega ``todos os campos`` da instância.

        Returns:
            ``set`` de todos os campos
        """
        fields = set()
        return fields.union(
            self.get_validation_fields(), self.get_non_required_fields()
        )

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union({"card", "type", "currency", "usage", "amount"})

    @classmethod
    def get_non_required_fields(cls) -> set:
        fields = super().get_non_required_fields()
        return fields.union({"installment_plan"})

    @classmethod
    def get_card_not_present_required_fields(cls):
        """
        Método get do ``set`` de ``required fields`` para :attr:`CARD_TYPE`
        quando o cartão é presente.

        Returns:
            ``set`` de campos
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


class InstallmentPlan(ZoopObject):
    INTEREST_FREE_MODE = "interest_free"
    WITH_INTEREST_MODE = "with_interest"

    INSTALLMENT_PLAN_MODES = {INTEREST_FREE_MODE, WITH_INTEREST_MODE}

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union({"mode", "number_installments"})

    def validate_custom_fields(self, **kwargs):
        errors = []
        if self.mode not in self.INSTALLMENT_PLAN_MODES:
            errors.append(
                FieldError(
                    "mode",
                    f"O mode é inválido! Deveria ser um dos "
                    f"dois tipos: {self.INSTALLMENT_PLAN_MODES}",
                )
            )

        if not InstallmentPlan._validate_number_installments(self.number_installments):
            errors.append(
                FieldError(
                    "number_installments",
                    f"O number_installments é inválido! Deveria ser de 1 até 12, "
                    f"e não {self.number_installments}",
                )
            )

        return errors

    @classmethod
    def _validate_number_installments(cls, number_installments):
        """
        Esse método verifica se:
            - number_installments é inteiro
            - number_installments é um valor inteiro entre 1 e 12 incluindo as bordas
        :return: bool
        """
        if not isinstance(number_installments, int):
            return False

        return number_installments >= 1 and number_installments <= 12
