from .base import (
    BusinessOrIndividualModel,
    Address,
    VerificationModel,
)
from ..exceptions import FieldError, ValidationError


class BankAccountVerificationModel(VerificationModel):
    """
    Have some bank account verification attributes.

    Attributes:
        deposit_check: boolean of verification
    """

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union({"deposit_check"})


class BankAccount(BusinessOrIndividualModel):
    """
    Represent a Bank Account.
    https://docs.zoop.co/reference#conta-banc%C3%A1ria

    The :attr:`RESOURCE` is used to identify this Model.
    Used to check against :attr:`.resource`!

    Attributes:
        account_number: account number
        bank_code: code of bank
        holder_name: name of owner
        routing_number: agency code in BR
        type: type of account

        address: Address model
        bank_name: name of bank
        country_code: country code
        customer: id of owner
        description: description
        debitable:  boolean of verification
        fingerprint: ?
        is_active: boolean of verification
        is_verified: boolean of verification
        last4_digits: last 4 digits of account number
        phone_number: phone number
        verification_checklist: VerificationCheckList model
    """

    RESOURCE = "bank_account"

    SAVING_TYPE = "Savings"
    CHECKING_TYPE = "Checking"
    TYPES = {SAVING_TYPE, CHECKING_TYPE}

    def init_custom_fields(
        self, type=None, address=None, verification_checklist=None, **kwargs
    ):
        """
        Initialize :attr:`address` as :class:`.Address`.\n

        Initialize :attr:`verification_checklist`
        as :class:`.BankAccountVerificationModel`.

        Args:
            type (str): value containing type
            address (dict or :class:`.Address`): address
            verification_checklist (dict or :class:`.BankAccountVerificationModel`): verifications  # noqa
            **kwargs:
        """
        self.set_identifier(**kwargs)
        self.validate_type(type)

        setattr(
            self, "address", Address.from_dict_or_instance(address, allow_empty=True)
        )

        setattr(
            self,
            "verification_checklist",
            BankAccountVerificationModel.from_dict_or_instance(
                verification_checklist, allow_empty=True
            ),
        )

    @classmethod
    def validate_type(cls, type):
        """
        Validate bank account ``type``

        Args:
            type (str): value of type to be validated

        Raises:
            ValidationError: when ``type`` is not in :attr:`TYPES`
        """
        if type not in cls.TYPES:
            raise ValidationError(
                cls, FieldError("type", f"type must one of {cls.TYPES}")
            )

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union({"type", "holder_name", "bank_code", "routing_number"})

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {
                "account_number",
                "address",
                "bank_name",
                "country_code",
                "customer",
                "debitable",
                "description",
                "fingerprint",
                "is_active",
                "is_verified",
                "last4_digits",
                "phone_number",
                "verification_checklist",
            }
        )
