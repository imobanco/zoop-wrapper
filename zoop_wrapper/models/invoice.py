from .base import PaymentMethod, ZoopObject
from ..exceptions import FieldError, ValidationError


class BaseModeObject(ZoopObject):
    """
    Um objeto base que possui modos de quantia e porcentagem
    """

    MODES = set()

    def init_custom_fields(self, mode=None, **kwargs):
        """
        É necessário configurar o :attr:`mode` antes pois
        ele influência no :meth:`get_validation_fields`
        """

        if mode not in self.MODES:
            raise ValidationError(
                self,
                FieldError(
                    "mode",
                    f"o valor {mode} é inválido! Possíveis modos são {self.MODES}",
                ),
            )

        setattr(self, "mode", mode)

    def get_mode_required_fields_mapping(self):
        raise NotImplementedError("Implemente o mapeamento!")

    def get_validation_fields(self):
        modes_required_fields_mapping = self.get_mode_required_fields_mapping()
        required_method = modes_required_fields_mapping.get(self.mode)
        return required_method()

    @classmethod
    def get_required_fields(cls):
        return {"mode"}

    @classmethod
    def get_percentage_required_fields(cls):
        fields = cls.get_required_fields()
        return fields.union({"percentage"})

    @classmethod
    def get_fixed_required_fields(cls):
        fields = cls.get_required_fields()
        return fields.union({"amount"})


class Fine(BaseModeObject):
    """
    Representa a multa!

    https://docs.zoop.co/docs/multa-juros-e-descontos#multa
    """

    FIXED = "FIXED"
    PERCENTAGE = "PERCENTAGE"
    MODES = {FIXED, PERCENTAGE}

    def get_mode_required_fields_mapping(self):
        return {
            self.FIXED: self.get_fixed_required_fields,
            self.PERCENTAGE: self.get_percentage_required_fields,
        }

    @classmethod
    def get_non_required_fields(cls):
        return {"start_date"}


class Interest(BaseModeObject):
    """
    Representa um juros!

    https://docs.zoop.co/docs/multa-juros-e-descontos#juros
    """

    DAILY_AMOUNT = "DAILY_AMOUNT"
    DAILY_PERCENTAGE = "DAILY_PERCENTAGE"
    MONTHLY_PERCENTAGE = "MONTHLY_PERCENTAGE"
    MODES = {DAILY_AMOUNT, DAILY_PERCENTAGE, MONTHLY_PERCENTAGE}

    def get_mode_required_fields_mapping(self):
        return {
            self.DAILY_AMOUNT: self.get_fixed_required_fields,
            self.DAILY_PERCENTAGE: self.get_percentage_required_fields,
            self.MONTHLY_PERCENTAGE: self.get_percentage_required_fields,
        }

    @classmethod
    def get_non_required_fields(cls):
        return {"start_date"}


class Discount(BaseModeObject):
    """
    Representa um desconto!

    https://docs.zoop.co/docs/multa-juros-e-descontos#descontos
    """

    FIXED = "FIXED"
    PERCENTAGE = "PERCENTAGE"
    MODES = {FIXED, PERCENTAGE}

    def get_mode_required_fields_mapping(self):
        return {
            self.FIXED: self.get_fixed_required_fields,
            self.PERCENTAGE: self.get_percentage_required_fields,
        }

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union({"limit_date"})


class BillingInstructions(ZoopObject):
    """
    Represents billing instructions (fine, interest and discount)

    Attributes:
        discount (list of :class:`.BillingConfiguration`): list of optional discount rules  # noqa
        interest (:class:`.BillingConfiguration`): optional interest rules
        late_fee (:class:`.BillingConfiguration`): optional fine rules
    """

    def init_custom_fields(self, late_fee=None, interest=None, discount=None, **kwargs):
        """
        Inicializa late_fee, interest e discount.

        Args:
            discount: dict or instance of BillingConfiguration model
            interest: dict or instance of BillingConfiguration model
            late_fee: dict or instance of BillingConfiguration model
            **kwargs: kwargs
        """
        if late_fee:
            setattr(
                self,
                "late_fee",
                Fine.from_dict_or_instance(late_fee),
            )

        if interest:
            setattr(
                self,
                "interest",
                Interest.from_dict_or_instance(interest),
            )

        if discount:
            if not isinstance(discount, list):
                discount = [discount]
            setattr(
                self,
                "discount",
                [Discount.from_dict_or_instance(item) for item in discount],
            )

    @classmethod
    def get_non_required_fields(cls):
        """
        Conjunto de campos não obrigatórios

        Returns:
            ``set`` de campos
        """
        fields = super().get_non_required_fields()
        return fields.union({"late_fee", "interest", "discount"})


class Invoice(PaymentMethod):
    """
    Represents a invoice ('boleto' in BR).
    https://docs.zoop.co/reference#boleto

    Attributes:
        billing_instructions (:class:`.BillingInstructions`): optional billing instructions  # noqa
        security_code_check (bool): verification of security code
    """

    RESOURCE = "boleto"

    def init_custom_fields(self, billing_instructions=None, **kwargs):
        """
        initialize :attr:`billing_instructions` with :class:`.BillingInstructions`

        Args:
            billing_instructions (dict or :class:`.BillingInstructions`): data
            **kwargs:
        """
        super().init_custom_fields(**kwargs)

        if billing_instructions:
            setattr(
                self,
                "billing_instructions",
                BillingInstructions.from_dict_or_instance(billing_instructions),
            )

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union({"expiration_date", "payment_limit_date"})

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {
                "accepted",
                "bank_code",
                "barcode",
                "billing_instructions",
                "body_instructions",
                "document_number",
                "downloaded",
                "fingerprint",
                "paid_at",
                "printed",
                "recipient",
                "reference_number",
                "sequence",
                "status",
                "url",
                "zoop_boleto_id",
            }
        )
