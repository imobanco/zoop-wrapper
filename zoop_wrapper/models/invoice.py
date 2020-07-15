from .base import PaymentMethod, ZoopObject
from ..exceptions import FieldError, ValidationError


class BillingConfiguration(ZoopObject):
    """
    Represents a billing configuration object.

    It has ``dynamic types``!

    Can be a ``Fee`` or a ``Discount``.\n
    And can be ``Fixed`` or ``Percentage``.

    So it can be ``Fee`` and ``Fixed``.
    Or ``Fee`` and ``Percentage``.
    Or ``Discount`` and ``Fixed``.
    Or ``Discount`` and ``Percentage``.

    ``Percentage`` can be just :attr:`PERCENTAGE_MODE` or
    :attr:`DAILY_PERCENTAGE_MODE` or
    :attr:`MONTHLY_PERCENTAGE_MODE`.

    ``Fixed`` is :attr:`FIXED_MODE`.

    The ``type identifier`` is the :attr:`mode` attribute value as in the Zoop API.\n
    The attr :attr:`is_discount` identify if it's a ``Discount`` or not.

    Attributes:
        amount (int): integer amount for :attr:`FIXED_MODE` in 'centavos'
        is_discount (bool): value representing if it's a ``Fee`` or ``Discount`` type
        limit_date (str): limit date of Discount type
        mode (str): value identifying if it's ``Fixed`` or ``Percentage`` type
        start_date (str): start date for :attr:`FIXED_MODE`
        percentage (float): float percentage for for ``Percentage`` types.
            It has a ``max`` of ``4 decimal points`` and
            is ``rounded up`` on the ``5º decimal point``
    """

    PERCENTAGE_MODE = "PERCENTAGE"
    DAILY_PERCENTAGE_MODE = "DAILY_PERCENTAGE"
    MONTHLY_PERCENTAGE_MODE = "MONTHLY_PERCENTAGE"
    FIXED_MODE = "FIXED"

    PERCENT_MODES = {PERCENTAGE_MODE, DAILY_PERCENTAGE_MODE, MONTHLY_PERCENTAGE_MODE}
    MODES = PERCENT_MODES.union({FIXED_MODE})

    def init_custom_fields(self, mode=None, is_discount=False, **kwarg):
        """
        call :meth:`set_type`

        Args:
            mode (str): value of mode
            is_discount: boolen of verification
            **kwarg: dict of kwargs
        """
        self.set_type(mode, is_discount)

    def validate_mode(self, mode):
        """
        Validate the ``mode``. It must be in :attr:`MODES`.

        Args:
            mode: ``mode`` to be validated

        Raises:
            :class:`.ValidationError`: when ``mode`` is not valid
        """
        if mode not in BillingConfiguration.MODES:
            if self._allow_empty:
                return False
            raise ValidationError(
                self, FieldError("mode", f"Must be one of {BillingConfiguration.MODES}")
            )
        return True

    def set_type(self, mode, is_discount):
        """
        set :attr:`mode` and :attr:`is_discount`

        Args:
            mode (str): mode
            is_discount (bool): value
        """
        self.validate_mode(mode)
        setattr(self, "mode", mode)
        setattr(self, "is_discount", is_discount)

    def get_validation_fields(self):
        """
        Get ``validation fields`` for instance.

        if ``type`` is ``Discount`` ``'fields'``
        is :meth:`get_discount_required_fields`\n

        else ``type`` is ``Fee``! ``'fields'``
        is :meth:`get_fee_required_fields`

        if ``type`` is  in :attr:`PERCENT_MODES` return ``'fields'`` union
        :meth:`get_percent_required_fields`\n

        else ``type`` is :attr:`FIXED_MODE` return ``'fields'`` union
        :meth:`get_fixed_required_fields`

        Returns:
            ``set`` of fields to be used on validation
        """
        if not self.validate_mode(self.mode):
            return self.get_required_fields()

        if self.is_discount:
            fields = self.get_discount_required_fields()
        else:
            fields = self.get_fee_required_fields()

        if self.mode in self.PERCENT_MODES:
            return fields.union(self.get_percent_required_fields())
        else:
            return fields.union(self.get_fixed_required_fields())

    def get_all_fields(self):
        """
        Get ``all fields`` for instance.
        Which are all the validation fields

        Returns:
            ``set`` of all fields
        """
        return self.get_validation_fields()

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union({"mode"})

    @classmethod
    def get_fee_required_fields(cls):
        """
        get ``set`` of ``required fields`` for ``Fee`` ``type``

        Returns:
            ``set`` of fields
        """
        fields = cls.get_required_fields()
        return fields.union({"start_date"})

    @classmethod
    def get_discount_required_fields(cls):
        """
        get ``set`` of ``required fields`` for ``Discount`` ``type``.

        Returns:
            ``set`` of fields
        """
        fields = cls.get_required_fields()
        return fields.union({"limit_date"})

    @classmethod
    def get_fixed_required_fields(cls):
        """
        get ``set`` of ``required fields`` for ``Fixed`` ``type``.

        Returns:
            ``set`` of fields
        """
        fields = cls.get_required_fields()
        return fields.union({"amount"})

    @classmethod
    def get_percent_required_fields(cls):
        """
        get ``set`` of ``required fields`` for ``Percent`` ``type``.

        Returns:
            ``set`` of fields
        """
        fields = cls.get_required_fields()
        return fields.union({"percentage"})

    @classmethod
    def from_dict_or_instance(cls, data, is_discount=False, **kwargs):
        """
        call ``super().from_dict_or_instance`` with
        the default of ``is_discount=False`` and passes kwargs.

        Args:
            data: dict of data or :class:`.Invoice`
            is_discount: boolean
            **kwargs: kwargs

        Returns:
            instance initialized of :class:`BillingConfiguration`
        """
        return super().from_dict_or_instance(data, is_discount=is_discount, **kwargs)


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
        initialize late_fee, interest and discount.

        Args:
            discount: dict or instance of BillingConfiguration model
            interest: dict or instance of BillingConfiguration model
            late_fee: dict or instance of BillingConfiguration model
            **kwargs: kwargs
        """
        setattr(
            self,
            "late_fee",
            BillingConfiguration.from_dict_or_instance(late_fee, allow_empty=True),
        )
        setattr(
            self,
            "interest",
            BillingConfiguration.from_dict_or_instance(interest, allow_empty=True),
        )
        if isinstance(discount, list):
            setattr(
                self,
                "discount",
                [
                    BillingConfiguration.from_dict_or_instance(
                        item, allow_empty=True, is_discount=True
                    )
                    for item in discount
                ],
            )
        else:
            setattr(
                self,
                "discount",
                [
                    BillingConfiguration.from_dict_or_instance(
                        discount, allow_empty=True, is_discount=True
                    )
                ],
            )

    @classmethod
    def get_required_fields(cls):
        """
        get set of required fields

        Returns:
            ``set`` of fields
        """
        fields = super().get_required_fields()
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

        setattr(
            self,
            "billing_instructions",
            BillingInstructions.from_dict_or_instance(
                billing_instructions, allow_empty=True
            ),
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
