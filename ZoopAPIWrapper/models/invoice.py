from ZoopAPIWrapper.models.base import (
    PaymentMethod, ZoopObject
)


class BillingConfiguration(ZoopObject):
    """
    Represents a billing configuration object.

    It has dynamics types!

    Can be a Fee or a Discount.
    Can be Fixed or Percentage.

    So it can be both Fee and Fixed. Or Fee and Percentage.
    Or Discount and Fixed. Or Discount and Percentage.

    Percentage can be just 'PERCENTAGE' or 'DAILY_PERCENTAGE' or
    'MONTHLY_PERCENTAGE'.

    The type identifier is the 'mode' value as in the Zoop API

    Attributes:
        PERCENTAGE_MODE: str representing this type
        DAILY_PERCENTAGE_MODE: str representing this type
        MONTHLY_PERCENTAGE_MODE: str representing this type
        FIXED_MODE: str representing this type

        PERCENT_MODES: set with all percent types
        MODES: set with all types

        is_discount: boolean representing if it's a Fee or Discount type
        mode: str identifyingg if it's Fixed or Percentage type
        start_date: start date of Fee type
        limit_date: limit date of Discount type
        amount: amount for Fixed type
        percentage: percentage for Percentage type
    """

    PERCENTAGE_MODE = 'PERCENTAGE'
    DAILY_PERCENTAGE_MODE = 'DAILY_PERCENTAGE'
    MONTHLY_PERCENTAGE_MODE = 'MONTHLY_PERCENTAGE'
    FIXED_MODE = 'FIXED'

    PERCENT_MODES = {PERCENTAGE_MODE, DAILY_PERCENTAGE_MODE,
                     MONTHLY_PERCENTAGE_MODE}
    MODES = PERCENT_MODES.union({FIXED_MODE})

    def init_custom_fields(self, mode=None, is_discount=False, **kwarg):
        """
        call set_type

        Args:
            mode: str of mode
            is_discount: boolen of verification
            **kwarg: dict of kwargs
        """
        if self._allow_empty:
            return

        self.set_type(mode, is_discount)

    @classmethod
    def validate_mode(cls, mode):
        """
        Validate the mode
        Args:
            mode: mode to be validated

        Raises:
            TypeError: when mode is not valid
        """
        if mode not in cls.MODES:
            raise TypeError(f'Mode not identified! Must be one of {cls.MODES}')

    def set_type(self, mode, is_discount):
        """
        set mode and is_discount

        Args:
            mode: mode str
            is_discount: boolean
        """
        self.validate_mode(mode)
        setattr(self, 'mode', mode)
        setattr(self, 'is_discount', is_discount)

    def get_validation_fields(self):
        """
        Get validation fields for instance.

        if type is Discount 'fields' is get_discount_required_fields()
        if type is Fee 'fields' is get_fee_required_fields()

        if type is Percent return 'fields' union
        get_percent_required_fields()

        if type is Fixed return 'fields' union
        get_fixed_required_fields()

        Raises:
            ValueError: when mode and is_discount is not set

        Returns: set of fields to validate
        """
        if self._allow_empty:
            return set()

        mode = getattr(self, 'mode', None)
        is_discount = getattr(self, 'is_discount', None)
        if is_discount is None or mode is None or mode not in self.MODES:
            raise ValueError('Must call config_mode before!')

        if is_discount:
            fields = self.get_discount_required_fields()
        else:
            fields = self.get_fee_required_fields()

        if mode in self.PERCENT_MODES:
            return fields.union(
                self.get_percent_required_fields()
            )
        else:
            return fields.union(
                self.get_fixed_required_fields()
            )

    def get_all_fields(self):
        """
        get all fields for instance.
        Which are all the validation fields

        Returns: set of all fields
        """
        return self.get_validation_fields()

    @classmethod
    def get_required_fields(cls):
        """
        get set of required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {'mode'}
        )

    @classmethod
    def get_fee_required_fields(cls):
        """
        get set of required fields for Fee Type

        Returns: set of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            {'start_date'}
        )

    @classmethod
    def get_discount_required_fields(cls):
        """
        get set of required fields for Discount Type

        Returns: set of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            {'limit_date'}
        )

    @classmethod
    def get_fixed_required_fields(cls):
        """
        get set of required fields for Fixed Type

        Returns: set of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            {'amount'}
        )

    @classmethod
    def get_percent_required_fields(cls):
        """
        get set of required fields for Percent Type

        Returns: set of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            {'percentage'}
        )

    @classmethod
    def from_dict_or_instance(cls, data, is_discount=False, **kwargs):
        """
        call super().from_dict_or_instance with
        default is_discount on kwargs passed.

        Args:
            data: dict of data or instance
            is_discount: boolean
            **kwargs: kwargs

        Returns: instance initialized of BillingConfiguration
        """
        return super().from_dict_or_instance(
            data,
            is_discount=is_discount,
            **kwargs
        )


class BillingInstructions(ZoopObject):
    """
    Represents billing instructions (fine, interest and discount)

    Attributes:
        late_fee: fine rules. BillingConfiguration model
        interest: interest rules. BillingConfiguration model
        discount: discount rules. BillingConfiguration model
    """

    def init_custom_fields(self, late_fee=None, interest=None,
                           discount=None, **kwargs):
        """
        initialize late_fee, interest and discount.

        Args:
            late_fee: dict or instance of BillingConfiguration model
            interest: dict or instance of BillingConfiguration model
            discount: dict or instance of BillingConfiguration model
            **kwargs: kwargs
        """
        setattr(
            self, 'late_fee',
            BillingConfiguration.from_dict_or_instance(
                late_fee, allow_empty=True))
        setattr(
            self, 'interest',
            BillingConfiguration.from_dict_or_instance(
                interest, allow_empty=True))
        setattr(
            self, 'discount',
            BillingConfiguration.from_dict_or_instance(
                discount, is_discount=True, allow_empty=True))

    @classmethod
    def get_required_fields(cls):
        """
        get set of required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {'late_fee', 'interest', 'discount'}
        )


class Invoice(PaymentMethod):
    """
    Represents
    This class and it's subclasses have attributes.

    Attributes:
        security_code_check: boolean of verification
    """
    RESOURCE = 'boleto'

    def init_custom_fields(self, billing_instructions=None, **kwargs):
        """
        initilize billin_instructions
        Args:
            billing_instructions: dict of data or BillinInstructions instance model
            **kwargs:
        """
        super().init_custom_fields(**kwargs)

        setattr(
            self, 'billing_instructions',
            BillingInstructions.from_dict_or_instance(billing_instructions,
                                                      allow_empty=True))

    @classmethod
    def get_required_fields(cls):
        """
        get set of required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {'expiration_date'}
        )

    @classmethod
    def get_non_required_fields(cls):
        """
        get set of non required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {'zoop_boleto_id', 'status', 'reference_number',
             'document_number', 'recipient', 'bank_code', 'sequence',
             'url', 'accepted', 'printed', 'downloaded', 'fingerprint',
             'paid_at', 'barcode', 'payment_limit_date', 'body_instructions',
             'billing_instructions'}
        )
