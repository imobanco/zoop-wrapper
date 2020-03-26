from ZoopAPIWrapper.models.base import (
    PaymentMethod, VerificationChecklist
)

class CardVerificationChecklist(VerificationChecklist):
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
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        security_code_check: boolean of verification
    """
    RESOURCE = 'card'

    __FIELDS = ["card_brand", "first4_digits", "last4_digits",
                "expiration_month", "expiration_year", "holder_name",
                "is_active", "is_valid", "is_verified", "fingerprint",
                "verification_checklist"]
