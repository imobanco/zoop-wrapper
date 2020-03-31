from ZoopAPIWrapper.models.base import (
    PaymentMethod, ZoopObject
)


class CostFee(ZoopObject):
    """
    Represent a cost configuration

    Attributes:
        mode: str
        start_date:
    """
    @classmethod
    def get_required_fields(cls):
        """
        get set of required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {'mode', 'start_date', 'percentage'}
        )


class DiscountFee(ZoopObject):
    @classmethod
    def get_required_fields(cls):
        """
        get set of required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {'mode', 'limit_date', 'amount'}
        )


class BillingInstructions(ZoopObject):
    def init_custom_fields(self, late_fee=None, interest=None,
                           discount=None, **kwargs):
        setattr(
            self, 'late_fee',
            CostFee.from_dict_or_instance(late_fee, allow_empty=True))
        setattr(
            self, 'interest',
            CostFee.from_dict_or_instance(interest, allow_empty=True))
        setattr(
            self, 'discount',
            DiscountFee.from_dict_or_instance(discount, allow_empty=True))

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
            {'expiration_date', 'billing_instructions'}
        )

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union(
            {'zoop_boleto_id', 'status', 'reference_number',
             'document_number', 'recipient', 'bank_code', 'sequence',
             'url', 'accepted', 'printed', 'downloaded', 'fingerprint',
             'paid_at', 'barcode', 'payment_limit_date', 'body_instructions'}
        )
