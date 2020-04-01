from ZoopAPIWrapper.models.base import (
    PaymentMethod, ZoopObject
)


class BillingConfiguration(ZoopObject):

    PERCENTAGE_MODE = 'PERCENTAGE'
    DAILY_PERCENTAGE_MODE = 'DAILY_PERCENTAGE'
    MONTHLY_PERCENTAGE_MODE = 'MONTHLY_PERCENTAGE'
    FIXED_MODE = 'FIXED'

    PERCENT_MODES = {PERCENTAGE_MODE, DAILY_PERCENTAGE_MODE, MONTHLY_PERCENTAGE_MODE}
    MODES = PERCENT_MODES.union({FIXED_MODE})

    def init_custom_fields(self, mode=None, is_discount=False, **kwarg):
        if self._allow_empty:
            return

        self.config_mode(mode, is_discount)

    def config_mode(self, mode, is_discount):
        if mode not in self.MODES:
            raise TypeError(f'Mode not identified! Must be one of {self.MODES}')
        setattr(self, 'mode', mode)
        setattr(self, 'is_discount', is_discount)

    def get_validation_fields(self):
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
        return self.get_validation_fields()

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union(
            {'mode'}
        )

    @classmethod
    def get_fee_required_fields(cls):
        fields = cls.get_required_fields()
        return fields.union(
            {'start_date'}
        )

    @classmethod
    def get_discount_required_fields(cls):
        fields = cls.get_required_fields()
        return fields.union(
            {'limit_date'}
        )

    @classmethod
    def get_fixed_required_fields(cls):
        fields = cls.get_required_fields()
        return fields.union(
            {'amount'}
        )

    @classmethod
    def get_percent_required_fields(cls):
        fields = cls.get_required_fields()
        return fields.union(
            {'percentage'}
        )

    @classmethod
    def from_dict_or_instance(cls, data, is_discount=False, **kwargs):
        return super().from_dict_or_instance(
            data,
            is_discount=is_discount,
            **kwargs
        )


class BillingInstructions(ZoopObject):
    def init_custom_fields(self, late_fee=None, interest=None,
                           discount=None, **kwargs):
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
        super().init_custom_fields(**kwargs)

        setattr(
            self, 'billing_instructions',
            BillingInstructions.from_dict_or_instance(billing_instructions,
                                                      allow_empty=True))

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union(
            {'expiration_date'}
        )

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union(
            {'zoop_boleto_id', 'status', 'reference_number',
             'document_number', 'recipient', 'bank_code', 'sequence',
             'url', 'accepted', 'printed', 'downloaded', 'fingerprint',
             'paid_at', 'barcode', 'payment_limit_date', 'body_instructions',
             'billing_instructions'}
        )
