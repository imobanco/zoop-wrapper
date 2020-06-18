from .base import PaymentMethod, VerificationModel


class CardVerificationChecklist(VerificationModel):
    """
    Represent a credit card verification

    Attributes:
        security_code_check: boolean of verification
    """

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union({"security_code_check"})


class Card(PaymentMethod):
    """
    Represent a Card.
    https://docs.zoop.co/reference#cart%C3%A3o

    The :attr:`RESOURCE` is used to identify this Model.
    Used to check against :attr:`.resource`!

    Attributes:
        card_brand: company name
        expiration_month: month of expiration
        expiration_year: year of expiration
        fingerprint: unique card identifier from company of card ?
        first4_digits: first 4 digits of card
        holder_name: owner name
        is_active: boolean of verification
        is_valid: boolean of verification
        is_verified: boolean of verification
        last4_digits: last 4 digits of card
        verification_checklist: CardVerificationChecklist model
    """

    RESOURCE = "card"

    def init_custom_fields(self, verification_checklist=None, **kwargs):
        """
        Initialize :attr:`verification_checklist` as
        :class:`CardVerificationChecklist`

        Args:
            verification_checklist: dict of data or :class:`CardVerificationChecklist`
            **kwargs: kwargs
        """
        setattr(
            self,
            "verification_checklist",
            CardVerificationChecklist.from_dict_or_instance(
                verification_checklist, allow_empty=True
            ),
        )

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union({"expiration_month", "expiration_year", "holder_name"})

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {
                "card_brand",
                "fingerprint",
                "first4_digits",
                "is_active",
                "is_valid",
                "is_verified",
                "last4_digits",
                "verification_checklist",
            }
        )
