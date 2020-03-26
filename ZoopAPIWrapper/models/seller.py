from ZoopAPIWrapper.models.base import ZoopBase, ZoopMarketPlaceModel, Address
from ZoopAPIWrapper.models.mixins import (
    BusinessOrIndividualMixin, classproperty)


class Seller(ZoopMarketPlaceModel, BusinessOrIndividualMixin):
    """
    Represent a seller.
    https://docs.zoop.co/reference#vendedor-1

    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    The TYPE attribute of this class is to be inherited and modified
    on IndividualSeller and BusinessSeller to be used on Zoop.api.

    Attributes:
        type: individual or business string
        status: pending or active string
        account_balance: amount of balance
        current_balance: curent amount of balance
        description: description
        statement_descriptor: ?
        mcc: ?
        show_profile_online:
        is_mobile: bolean of verification
        decline_on_fail_security_code: bolean of verification
        decline_on_fail_zipcode: bolean of verification
        delinquent: bolean of verification
        payment_methods: ?
        default_debit: ?
        default_credit: ?
        merchant_code: ?
        terminal_code: ?
    """
    RESOURCE = 'seller'

    TYPE = None

    __FIELDS = ["status", "type", "account_balance", "current_balance",
                "description", "statement_descriptor", "mcc",
                "show_profile_online", "is_mobile",
                "decline_on_fail_security_code",
                "decline_on_fail_zipcode",
                "delinquent", "payment_methods", "default_debit",
                "default_credit", "merchant_code", "terminal_code"]

    def __init__(self, status=None, account_balance=None, current_balance=None,
                 description=None, statement_descriptor=None, mcc=None,
                 show_profile_online=None, is_mobile=None,
                 decline_on_fail_security_code=None,
                 decline_on_fail_zipcode=None, delinquent=None,
                 payment_methods=None, default_debit=None, default_credit=None,
                 merchant_code=None, terminal_code=None, type=None, **kwargs):
        super().__init__(**kwargs)

        self.status = status
        self.account_balance = account_balance
        self.current_balance = current_balance
        self.description = description
        self.statement_descriptor = statement_descriptor
        self.mcc = mcc
        self.show_profile_online = show_profile_online
        self.is_mobile = is_mobile
        self.decline_on_fail_security_code = decline_on_fail_security_code
        self.decline_on_fail_zipcode = decline_on_fail_zipcode
        self.delinquent = delinquent
        self.payment_methods = payment_methods
        self.default_debit = default_debit
        self.default_credit = default_credit
        self.merchant_code = merchant_code
        self.terminal_code = terminal_code

        self.type = type

    # noinspection PyMethodParameters
    @classproperty
    def business_class(cls):
        """
        getter for business class
        Returns: BusinessSeller
        """
        return BusinessSeller

    # noinspection PyMethodParameters
    @classproperty
    def individual_class(cls):
        """
        getter for individual class
        Returns: IndividualSeller
        """
        return IndividualSeller

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
        construct a IndividualSeller or BusinessSeller
        depending on BusinessOrIndividualMixin.
        Factory pattern

        Args:
            data: dict of data

        Returns: instance initialized of Seller
        """
        klass = cls.get_class(data)
        return klass.from_dict(data)

    @classmethod
    def get_type(cls):
        """
        getter for TYPE attribute

        Raises:
            ValueError: when called from Seller

        Returns: TYPE attribute
        """
        if cls.TYPE is None:
            raise ValueError('TYPE must be set!')
        return cls.TYPE


class Owner(ZoopBase):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        address: Address model
        birthdate: birthdate
        email: email
        first_name: first name
        last_name: last name
        phone_number: phone number
        taxpayer_id: cpf
    """
    __FIELDS = ["first_name", "last_name", "email",
                "taxpayer_id", "phone_number",
                "birthdate", "address"]

    def __init__(self, first_name, last_name, email,
                 taxpayer_id, phone_number, birthdate,
                 address=None, **kwargs):
        super().__init__(**kwargs)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.taxpayer_id = taxpayer_id
        self.phone_number = phone_number
        self.birthdate = birthdate
        self.address = Address.from_dict_or_instance(address)

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


class IndividualSeller(Seller, Owner):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    The TYPE attribute of this class is used on Zoop.api.

    Attributes:
        website: website url?
        facebook: facebook profile url?
        twitter: twitter profile url?
    """
    __FIELDS = ["website", "facebook", "twitter"]

    TYPE = 'individuals'

    def __init__(self, website=None, facebook=None,
                 twitter=None, **kwargs):
        super().__init__(**kwargs)

        self.website = website
        self.facebook = facebook
        self.twitter = twitter

    @classmethod
    def from_dict(cls, data):
        """
        construct a instance of this class from dict

        Args:
            data: dict of data

        Returns: instance initialized of class or None
        """
        return cls._from_dict(**data)

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


class BusinessSeller(Seller):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    The TYPE attribute of this class is used on Zoop.api.

    Attributes:
        ein: (Employer Identification Number) is equivalent to CNPJ
        business_name: name
        business_phone: phone number
        business_email: email
        business_website: website url
        business_opening_date: date of openning
        owner: Owner
        business_address: Address model
        business_description: description
        business_facebook: facebook profile url?
        business_twitter: twitter profile url?
    """
    TYPE = 'business'

    __FIELDS = ["business_name", "business_phone",
                "business_email", "business_website",
                "business_description", "business_opening_date",
                "business_facebook", "business_twitter", "ein",
                "owner", "business_address"]

    def __init__(self, ein, business_name, business_phone,
                 business_email, business_website,
                 business_opening_date, owner, business_address,
                 business_description=None, business_facebook=None,
                 business_twitter=None, **kwargs):
        super().__init__(**kwargs)

        self.ein = ein
        self.business_name = business_name
        self.business_phone = business_phone
        self.business_email = business_email
        self.business_website = business_website
        self.business_opening_date = business_opening_date

        self.business_address = Address.from_dict_or_instance(business_address)
        self.owner = Owner.from_dict_or_instance(owner)
        self.business_description = business_description
        self.business_facebook = business_facebook
        self.business_twitter = business_twitter

    @classmethod
    def from_dict(cls, data):
        """
        construct a instance of this class from dict

        Args:
            data: dict of data

        Returns: instance initialized of class or None
        """
        return cls._from_dict(**data)

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
