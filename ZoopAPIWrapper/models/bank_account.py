from ZoopAPIWrapper.models.base import ZoopBase, ZoopModel, Address
from ZoopAPIWrapper.models.mixins import (
    BusinessOrIndividualMixin, classproperty)


class VerificationChecklist(ZoopBase):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        postal_code_check: boolean of verification
        address_line1_check: boolean of verification
        deposit_check: boolean of verification
    """
    __FIELDS = ["postal_code_check", "address_line1_check",
                "deposit_check"]

    def __init__(self, postal_code_check, address_line1_check,
                 deposit_check, **kwargs):
        super().__init__(**kwargs)

        self.postal_code_check = postal_code_check
        self.address_line1_check = address_line1_check
        self.deposit_check = deposit_check

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


class BankAccount(ZoopModel, BusinessOrIndividualMixin):
    """
    Represent a Bank Account.
    https://docs.zoop.co/reference#conta-banc%C3%A1ria

    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

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

    __FIELDS = ["holder_name", "description",
                "bank_name", "bank_code", "type",
                "last4_digits", "account_number",
                "country_code", "routing_number",
                "phone_number", "is_active", "is_verified",
                "debitable", "customer", "fingerprint",
                "address", "verification_checklist"]

    def __init__(self, holder_name, bank_code, routing_number,
                 account_number,
                 description=None, bank_name=None, type=None,
                 country_code=None, phone_number=None,
                 is_active=None, is_verified=None,
                 debitable=None, customer=None, fingerprint=None,
                 address=None, verification_checklist=None,
                 last4_digits=None, **kwargs):
        super().__init__(**kwargs)

        self.holder_name = holder_name
        self.bank_code = bank_code
        self.routing_number = routing_number
        self.account_number = account_number

        self.description = description
        self.bank_name = bank_name
        self.type = type
        self.last4_digits = last4_digits
        self.country_code = country_code
        self.phone_number = phone_number
        self.is_active = is_active
        self.is_verified = is_verified
        self.debitable = debitable
        self.customer = customer
        self.fingerprint = fingerprint

        self.address = AddressModel.from_dict_or_instance(address)
        self.verification_checklist = VerificationChecklist\
            .from_dict_or_instance(verification_checklist)

    # noinspection PyMethodParameters
    @classproperty
    def business_class(cls):
        """
        getter for individual class
        Returns: IndividualBankAccount
        """
        return BusinessBankAccount

    # noinspection PyMethodParameters
    @classproperty
    def individual_class(cls):
        """
        getter for business class
        Returns: BusinessBankAccount
        """
        return IndividualBankAccount

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

    @classmethod
    def from_dict(cls, data):
        """
        construct a IndividualBankAccount or BusinessBankAccount
        depending on BusinessOrIndividualMixin.
        Factory pattern

        Args:
            data: dict of data

        Returns: instance initialized of BankAccount
        """
        klass = BankAccount.get_class(data)
        return klass.from_dict(data)


class BusinessBankAccount(BankAccount):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        ein: (Employer Identification Number) is equivalent to CNPJ
    """
    __FIELDS = ["ein"]

    def __init__(self, ein, **kwargs):
        super().__init__(**kwargs)

        self.ein = ein

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

    @classmethod
    def from_dict(cls, data):
        """
        construct a instance of this class from dict.

        Args:
            data: dict of data

        Returns: instance initialized of class or None
        """
        return cls._from_dict(**data)


class IndividualBankAccount(BankAccount):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        taxpayer_id: cpf
    """
    __FIELDS = ["taxpayer_id"]

    def __init__(self, taxpayer_id, **kwargs):
        super().__init__(**kwargs)

        self.taxpayer_id = taxpayer_id

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

    @classmethod
    def from_dict(cls, data):
        """
        construct a instance of this class from dict

        Args:
            data: dict of data

        Returns: instance initialized of class or None
        """
        return cls._from_dict(**data)
