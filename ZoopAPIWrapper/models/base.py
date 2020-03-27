from ZoopAPIWrapper.utils import get_logger
from ZoopAPIWrapper.exceptions import ValidationError


logger = get_logger('models')


class ZoopBase(object):
    """
    This class represent a bare ZoopBase object.

    A instance of this class doesn't have attributes.

    Attributes:
        __allow_empty: boolean
    """

    def __init__(self, allow_empty=False, **kwargs):
        """
        constructor

        Args:
            **kwargs: dictionary of args
        """

        for field_name in self.get_fields():
            my_value = getattr(self, field_name, None)
            if my_value is not None:
                continue

            value = kwargs.get(field_name, None)
            setattr(self, field_name, value)

        self.__allow_empty = allow_empty

        self.validate_required_fields()

    @classmethod
    def from_dict(cls, data, allow_empty=False):
        """
        construct a instance of this class from dict

        Args:
            data: dict of data
            allow_empty: boolean

        Returns: instance initialized of cls
        """
        if data is None:
            _data = {}
        else:
            _data = {key: value for key, value in data.items()}

        _data['allow_empty'] = allow_empty
        return cls(**_data)

    @classmethod
    def from_dict_or_instance(cls, data, allow_empty=False):
        """
        check if data is already a ZoopModel or subclass.
        If not call from_dict

        Args:
            data: dict of data or instance

        Returns: instance initialized of cls
        """
        if isinstance(data, cls):
            return data
        else:
            return cls.from_dict(data, allow_empty)

    def to_dict(self):
        """
        serialize the instance to dict
        Returns: dict of instance
        """
        data = {}
        for field in self.get_fields():
            try:
                """our attr may be a ZoopBase instance.
                Let's try to get its serialized value!"""
                attr = getattr(self, field).to_dict()
            except AttributeError:
                """our attr doesn't have to_dict() method.
                Oh snap! It's not a ZoopBase instance!"""
                attr = getattr(self, field)

            if attr is not None or self.__allow_empty:
                data[field] = attr

        return data

    def validate_required_fields(self, raise_exception=None):
        """
        Validate all required_fields

        Args:
            raise_exception: boolean to raise or not exception

        Raises:
            ValidationError: if there's some required_field missing
            and __allow_empty is false and raise_exception is true

        """
        errors = []
        for required_field in self.get_required_fields():
            value = getattr(self, required_field, None)
            if value is None:
                errors.append(required_field)

        if (
                errors and
                (
                        raise_exception or
                        (
                                raise_exception is None and
                                not self.__allow_empty
                        )
                )
        ):
            raise ValidationError(errors)

    @classmethod
    def get_fields(cls):
        """
        list of all fields

        Returns: list of fields
        """
        return cls.get_required_fields() + cls.get_non_required_fields()

    @classmethod
    def get_required_fields(cls):
        """
        list of required fields

        Returns: list of fields
        """
        return []

    @classmethod
    def get_non_required_fields(cls):
        """
        list of non required fields

        Returns: list of fields
        """
        return []


class ZoopModel(ZoopBase):
    # noinspection PyUnresolvedReferences
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        id: identifier string
        resource: type string
        uri: uri string
        created_at: date of creation
        updated_at: date of update
        metadata: dict with metadata
    """

    @classmethod
    def get_non_required_fields(cls):
        """
        list of non required fields

        Returns: list of fields
        """
        fields = super().get_non_required_fields()
        fields.extend(
            ["id", "resource", "uri", "created_at", "updated_at", "metadata"]
        )
        return fields


class ZoopMarketPlaceModel(ZoopModel):
    # noinspection PyUnresolvedReferences
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        marketplace_id: identifier string
    """

    @classmethod
    def get_non_required_fields(cls):
        """
        list of non required fields

        Returns: list of fields
        """
        fields = super().get_non_required_fields()
        fields.extend(
            ['marketplace_id']
        )
        return fields


class AddressModel(ZoopBase):
    # noinspection PyUnresolvedReferences
    """
    This class and it's subclasses have attributes.

    Attributes:
        line1: complete street name
        line2: number
        line3: complement
        neighborhood: neighborhood
        city: city
        state: Código ISO 3166-2 para o estado
        postal_code: postal code
        country_code: ISO 3166-1 alpha-2 - códigos de país de duas letras
    """

    @classmethod
    def get_non_required_fields(cls):
        """
        list of non required fields

        Returns: list of fields
        """
        fields = super().get_non_required_fields()
        fields.extend(
            ["line1", "line2", "line3",
             "neighborhood", "city", "state",
             "postal_code", "country_code"]
        )
        return fields


class OwnerModel(ZoopBase):
    # noinspection PyUnresolvedReferences
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

    def __init__(self, address, **kwargs):
        setattr(self, 'address', AddressModel.from_dict_or_instance(address, allow_empty=True))

        super().__init__(**kwargs)

    @classmethod
    def get_required_fields(cls):
        """
        list of required fields

        Returns: list of fields
        """
        fields = super().get_required_fields()
        fields.extend(
            ["first_name", "last_name", "email",
             "taxpayer_id", "phone_number",
             "birthdate", "address"]
        )
        return fields

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class SocialModel(ZoopBase):
    # noinspection PyUnresolvedReferences
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        facebook: facebook profile url?
        twitter: twitter profile url?
    """
    __FIELDS = ["facebook", "twitter"]

    def __init__(self, facebook=None,
                 twitter=None, **kwargs):
        super().__init__(**kwargs)

        self.facebook = facebook
        self.twitter = twitter

    @property
    def get_fields(self):
        """
        the fields of ZoopBase are it's
        __FIELDS extended with it's father fields.
        it's important to be a new list (high order function)
        Returns: new list of attributes
        """
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


class FinancialModel(ZoopBase):
    # noinspection PyUnresolvedReferences
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        status: pending or active string
        account_balance: amount of balance
        current_balance: curent amount of balance
        description: description
        delinquent: bolean of verification
        payment_methods: ?
        default_debit: ?
        default_credit: ?
    """
    __FIELDS = ['status', 'account_balance', 'current_balance',
                'description', 'delinquent', 'payment_methods',
                'default_debit', 'default_credit']


    @property
    def get_fields(self):
        """
        the fields of ZoopBase are it's
        __FIELDS extended with it's father fields.
        it's important to be a new list (high order function)
        Returns: new list of attributes
        """
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


class VerificationChecklist(ZoopBase):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        postal_code_check: boolean of verification
        address_line1_check: boolean of verification
    """
    __FIELDS = ["postal_code_check", "address_line1_check"]


    @property
    def get_fields(self):
        """
        the fields of ZoopBase are it's
        __FIELDS extended with it's father fields.
        it's important to be a new list (high order function)
        Returns: new list of attributes
        """
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)


class PaymentMethod(ZoopModel):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        description: text description
        customer: uuid id
        address: Address Model
    """
    __FIELDS = ['description', 'customer', 'address']

    @property
    def get_fields(self):
        """
        the fields of ZoopBase are it's
        __FIELDS extended with it's father fields.
        it's important to be a new list (high order function)
        Returns: new list of attributes
        """
        super_fields = super().fields
        super_fields.extend(self.__FIELDS)
        return list(super_fields)
