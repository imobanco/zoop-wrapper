from ZoopAPIWrapper.models.base import (
    PaymentMethod
)


class Invoice(PaymentMethod):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        security_code_check: boolean of verification
    """
    RESOURCE = 'boleto'

    __FIELDS = ['zoop_boleto_id', 'status', "reference_number",
                "document_number", "expiration_date", "payment_limit_date",
                "recipient", "bank_code", "sequence", "url", "accepted",
                "printed", "downloaded", "fingerprint", "paid_at", "barcode"]