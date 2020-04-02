from ZoopAPIWrapper.models.base import (
    PaymentMethod, VerificationModel
)


class CardVerificationChecklist(VerificationModel):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        security_code_check: boolean of verification
    """
    __FIELDS = ["security_code_check"]

    def __init__(self, security_code_check, **kwargs):
        super().__init__(**kwargs)

        self.security_code_check = security_code_check

    @property
    def fields(self):
        """
        the fields of ZoopBase are it's
        __FIELDS extended with it's father fields.
        it's important to be a new list (high order function)
        Returns: new list of attributes
        """
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


class Card(PaymentMethod):
    """
    Represent a Card.
    https://docs.zoop.co/reference#cart%C3%A3o

    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        card_brand: company name
        first4_digits: first 4 digits of card
        last4_digits: last 4 digits of card
        expiration_month: month of expiration
        expiration_year: year of expiration
        holder_name: owner name
        is_active: boolean of verification
        is_valid: boolean of verification
        is_verified: boolean of verification
        fingerprint: ?
        verification_checklist: CardVerificationChecklist model
    """
    RESOURCE = 'card'

    __FIELDS = ["card_brand", "first4_digits", "last4_digits",
                "expiration_month", "expiration_year", "holder_name",
                "is_active", "is_valid", "is_verified", "fingerprint",
                "verification_checklist"]

    def __init__(self, card_brand, first4_digits, last4_digits,
                 expiration_month, expiration_year, holder_name,
                 is_active=None, is_valid=None, is_verified=None, fingerprint=None,
                 verification_checklist=None, **kwargs):
        super().__init__(**kwargs)

        self.card_brand = card_brand
        self.first4_digits = first4_digits
        self.last4_digits = last4_digits
        self.expiration_month = expiration_month
        self.expiration_year = expiration_year
        self.holder_name = holder_name
        self.is_active = is_active
        self.is_valid = is_valid
        self.is_verified = is_verified
        self.fingerprint = fingerprint
        self.verification_checklist = CardVerificationChecklist\
            .from_dict_or_instance(verification_checklist)

    @property
    def fields(self):
        """
        the fields of ZoopBase are it's
        __FIELDS extended with it's father fields.
        it's important to be a new list (high order function)
        Returns: new list of attributes
        """
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)
