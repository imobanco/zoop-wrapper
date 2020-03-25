from ZoopAPIWrapper.utils import get_logger


logger = get_logger('models')


class ZoopBase:
    """
    This class represent a bare ZoopBase object.

    A instance of this class doesn't have attributes.

    This class has the attribute __FIELDS with the list of attributes it has.
    The purpose of this is to construct the dict of the object.
    """
    __FIELDS = []

    def __init__(self, *args, **kwargs):
        """
        constructor

        Args:
            *args:
            **kwargs:
        """
        pass

    @classmethod
    def _from_dict(cls, **entries):
        """
        construct a instance of this class from **entries

        Args:
            **entries:

        Returns: instance initialized of class
        """
        return cls(**entries)

    @classmethod
    def from_dict(cls, data):
        """
        construct a instance of this class from dict

        Args:
            data: dict of data

        Returns: instance initialized of class
        """
        return cls._from_dict(**data)

    def to_dict(self):
        """
        serialize the instance to dict
        Returns: dict of instance
        """
        data = {}
        for field in self.fields:
            try:
                """our attr may be a ZoopBase instance.
                Let's try to get its serialized value!"""
                attr = getattr(self, field).to_dict()
            except AttributeError:
                """our attr doesn't have to_dict() method.
                Oh snap! It's not a ZoopBase instance!"""
                attr = getattr(self, field)

            if attr is not None:
                """only serialize values which are not None"""
                data[field] = attr

        return data

    @property
    def fields(self):
        """
        the fields of ZoopBase are it's __FIELDS attrs.
        it's important to be a new list (high order function)
        Returns: new list of attributes
        """
        return list(self.__FIELDS)


class ZoopModel(ZoopBase):
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
    __FIELDS = ["id", "resource", "uri", "created_at", "updated_at", "metadata"]

    def __init__(self, id=None, resource=None, uri=None,
                 created_at=None, updated_at=None,
                 metadata=None, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.resource = resource
        self.uri = uri

        self.created_at = created_at
        self.updated_at = updated_at
        self.metadata = metadata

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


class ZoopMarketPlaceModel(ZoopModel):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        marketplace_id: identifier string
    """
    __FIELDS = ["marketplace_id"]

    def __init__(self, marketplace_id=None, **kwargs):
        super().__init__(**kwargs)

        self.marketplace_id = marketplace_id

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


class AddressModel(ZoopBase):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

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
    __FIELDS = ["line1", "line2", "line3",
                "neighborhood", "city", "state",
                "postal_code", "country_code"]

    def __init__(self, line1, line2, line3,
                 neighborhood, city, state,
                 postal_code, country_code, **kwargs):
        super().__init__(**kwargs)

        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country_code = country_code

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


class OwnerModel(ZoopBase):
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
                 address, **kwargs):
        super().__init__(**kwargs)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.taxpayer_id = taxpayer_id
        self.phone_number = phone_number
        self.birthdate = birthdate
        self.address = AddressModel.from_dict(address)

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


class SocialModel(ZoopBase):
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


class FinancialModel(ZoopBase):
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

    def __init__(self, status=None, account_balance=None, current_balance=None,
                 description=None, delinquent=None, payment_methods=None,
                 default_debit=None, default_credit=None, **kwargs):
        super().__init__(**kwargs)

        self.status = status
        self.account_balance = account_balance
        self.current_balance = current_balance
        self.description = description
        self.delinquent = delinquent
        self.payment_methods = payment_methods
        self.default_debit = default_debit
        self.default_credit = default_credit

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