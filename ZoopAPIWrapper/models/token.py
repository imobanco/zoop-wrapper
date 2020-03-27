from ZoopAPIWrapper.models.base import (
    ZoopModel
)
from ZoopAPIWrapper.models.bank_account import BankAccount
from ZoopAPIWrapper.models.card import Card
from ZoopAPIWrapper.models.mixins import BusinessOrIndividualMixin
from ZoopAPIWrapper.utils import classproperty, get_logger


logger = get_logger('models')


class Token(ZoopModel):
    """
    Token is a resource used to link a BankAccount Or Card and a Customer
    https://docs.zoop.co/reference#token-1

    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        type: bank_account or card
        used: boolean of verification
    """
    RESOURCE = 'token'

    __FIELDS = ['type', 'used']

    def __init__(self, type, used, **kwargs):
        super().__init__(**kwargs)

        self.type = type
        self.used = used

    @classmethod
    def from_dict(cls, data):
        card = data.get('card', False)
        bank_account = data.get('bank_account', False)

        if card:
            return CardToken.from_dict(data)

        if bank_account:
            return BankAccountToken.from_dict(data)

        return super().from_dict(data)

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


class BankAccountToken(BusinessOrIndividualMixin, Token):
    """
    Token is a resource used to link a BankAccount and a Customer
    https://docs.zoop.co/reference#post_v1-marketplaces-marketplace-id-bank-accounts-tokens

    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        holder_name: name of owner
        bank_code: number of card
        routing_number: month of expiration
        account_number: year of expiration
        type: security code
        bank_account: BankAccount model
    """
    __FIELDS = ['holder_name', 'card_number', 'expiration_month',
                'expiration_year', 'security_code', 'card']

    def __init__(self, holder_name, bank_code, routing_number,
                 account_number, type,
                 bank_account=None, **kwargs):
        super().__init__(type=None, used=None, **kwargs)

        self.holder_name = holder_name
        self.bank_code = bank_code
        self.routing_number = routing_number
        self.account_number = account_number
        self.type = type
        try:
            self.bank_account = BankAccount.from_dict(bank_account)
        except TypeError as e:
            e.args = (f'{BankAccount} could not be created!',)
            logger.warning(e)
            self.bank_account = None

    # noinspection PyMethodParameters
    @classproperty
    def business_class(cls):
        return BusinessBankAccountToken

    # noinspection PyMethodParameters
    @classproperty
    def individual_class(cls):
        return IndividualBankAccountToken

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


class BusinessBankAccountToken(BankAccountToken):
    """
    Token is a resource used to link a BankAccount and a Customer
    https://docs.zoop.co/reference#post_v1-marketplaces-marketplace-id-bank-accounts-tokens

    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        ein: CNPJ
    """
    __FIELDS = ['ein']

    def __init__(self, ein, **kwargs):
        super().__init__(**kwargs)

        self.ein = ein

    @classmethod
    def from_dict(cls, data):
        """
        construct a instance of this class from dict

        Args:
            data: dict of data

        Returns: instance initialized of cls
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


class IndividualBankAccountToken(BankAccountToken):
    """
    Token is a resource used to link a BankAccount and a Customer
    https://docs.zoop.co/reference#post_v1-marketplaces-marketplace-id-bank-accounts-tokens

    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        taxpayer_id: CPF
    """
    __FIELDS = ['taxpayer_id']

    def __init__(self, taxpayer_id, **kwargs):
        super().__init__(**kwargs)

        self.taxpayer_id = taxpayer_id

    @classmethod
    def from_dict(cls, data):
        """
        construct a instance of this class from dict

        Args:
            data: dict of data

        Returns: instance initialized of cls
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


class CardToken(Token):
    """
    Token is a resource used to link a Card and a Customer
    https://docs.zoop.co/reference#post_v1-marketplaces-marketplace-id-cards-tokens

    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        holder_name: name of owner
        card_number: number of card
        expiration_month: month of expiration
        expiration_year: year of expiration
        security_code: security code
        card: Card model
    """
    __FIELDS = ['holder_name', 'card_number', 'expiration_month',
                'expiration_year', 'security_code', 'card']

    def __init__(self, holder_name, card_number, expiration_month,
                 expiration_year, security_code,
                 card=None, **kwargs):
        super().__init__(type=None, used=None, **kwargs)

        self.holder_name = holder_name
        self.card_number = card_number
        self.expiration_month = expiration_month
        self.expiration_year = expiration_year
        self.security_code = security_code
        try:
            self.card = Card.from_dict_or_instance(card)
        except TypeError as e:
            e.args = (f'{Card} could not be created!',)
            logger.warning(e)
            self.card = None

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
