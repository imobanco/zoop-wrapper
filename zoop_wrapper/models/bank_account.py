from zoop_wrapper.models.base import (
    BusinessOrIndividualModel, Address, VerificationModel)
from zoop_wrapper.exceptions import FieldError, ValidationError


class BankAccountVerificationModel(VerificationModel):
    """
    Have some bank account verification attributes.

    Attributes:
        deposit_check: boolean of verification
    """

    @classmethod
    def get_required_fields(cls):
        """
        get set of required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {'deposit_check'}
        )


class BankAccount(BusinessOrIndividualModel):
    """
    Represent a Bank Account.
    https://docs.zoop.co/reference#conta-banc%C3%A1ria

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        SAVING_TYPE: str for saving type
        CHECKING_TYPE: str for checking type
        TYPES: set of types

        type: type of account
        account_number: account number
        bank_code: code of bank
        holder_name: name of owner
        routing_number: agency code in BR

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
    RESOURCE = 'bank_account'

    SAVING_TYPE = 'Savings'
    CHECKING_TYPE = 'Checking'
    TYPES = {SAVING_TYPE, CHECKING_TYPE}

    def init_custom_fields(self, type=None, address=None,
                           verification_checklist=None,
                           **kwargs):
        """
        Initialize address as Address model.
        Initialize verification_checklist
        as BankAccountVerificationModel model.

        Args:
            type: str containing type
            address: dict of data or instance of Address
            verification_checklist: dict of data or
                instance of BankAccountVerificationModel
            **kwargs:
        """
        self.set_identifier(**kwargs)
        self.validate_type(type)

        setattr(
            self, 'address',
            Address.from_dict_or_instance(address, allow_empty=True))

        setattr(
            self, 'verification_checklist',
            BankAccountVerificationModel.from_dict_or_instance(
                verification_checklist, allow_empty=True))

    @classmethod
    def validate_type(cls, type):
        """
        Validate bank account type

        Args:
            type: str of type to be validated

        Raises:
            ValidationError: when type is not in valid TYPES
        """
        if type not in cls.TYPES:
            raise ValidationError(cls, FieldError('type', f'type must one of {cls.TYPES}'))

    @classmethod
    def get_required_fields(cls):
        """
        get set of required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {"type", "holder_name", "bank_code",
             "routing_number"}
        )

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {"account_number", "description", "bank_name",
             "last4_digits", "country_code", "phone_number",
             "is_active", "is_verified", "debitable", "customer",
             "fingerprint", "address", "verification_checklist"}
        )
