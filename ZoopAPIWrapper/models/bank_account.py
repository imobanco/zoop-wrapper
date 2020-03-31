from ZoopAPIWrapper.models.base import (
    BusinessOrIndividualModel, Address, VerificationModel)


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
        type: type of account
        verification_checklist: VerificationCheckList model
    """
    RESOURCE = 'bank_account'

    def init_custom_fields(self, address=None, verification_checklist=None,
                           **kwargs):
        self.set_identifier(**kwargs)

        setattr(self, 'address',
                Address.from_dict_or_instance(address, allow_empty=True))

        setattr(
            self,
            'verification_checklist',
            BankAccountVerificationModel.from_dict_or_instance(
                verification_checklist, allow_empty=True))

    @classmethod
    def get_required_fields(cls):
        """
        get set of required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {"holder_name", "description",
             "bank_name", "bank_code"}
        )

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {"type", "last4_digits", "account_number",
             "country_code", "routing_number", "phone_number",
             "is_active", "is_verified", "debitable", "customer",
             "fingerprint", "address", "verification_checklist"}
        )

    @classmethod
    def from_dict_and_seller(cls, seller, data):
        data['holder_name'] = seller.full_name
        return cls.from_dict(data)
