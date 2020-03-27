from ZoopAPIWrapper.utils import get_logger


logger = get_logger('models')


class ZoopBase:
    """
    This class represent a bare ZoopBase object.

    A instance of this class doesn't have attributes.

    This class has the attribute __FIELDS with the list of attributes it has.
    The purpose of this is to construct the dict of the object.
    """

    def __init__(self, **kwargs):
        """
        constructor

        Args:
            **kwargs: dictionary of args
        """
        for field_name in self.fields:
            value = kwargs.get(field_name, None)
            setattr(self, field_name, value)

        self.validate_required_field()

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

        Returns: instance initialized of cls
        """
        return cls._from_dict(**data)

    @classmethod
    def from_dict_or_instance(cls, data):
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
            return cls.from_dict(data)

    def to_dict(self):
        """
        serialize the instance to dict
        Returns: dict of instance
        """
        data = {}
        for required_field in self.required_fields:
            try:
                """our attr may be a ZoopBase instance.
                Let's try to get its serialized value!"""
                attr = getattr(self, required_field).to_dict()
            except AttributeError:
                """our attr doesn't have to_dict() method.
                Oh snap! It's not a ZoopBase instance!"""
                attr = getattr(self, required_field)

            if attr is None:
                self.validate_required_field()

            data[required_field] = attr

        for non_required_field in self.non_required_fields:
            try:
                """our attr may be a ZoopBase instance.
                Let's try to get its serialized value!"""
                attr = getattr(self, non_required_field).to_dict()
            except AttributeError:
                """our attr doesn't have to_dict() method.
                Oh snap! It's not a ZoopBase instance!"""
                attr = getattr(self, non_required_field)

            if attr is not None:
                """only serialize values which are not None"""
                data[non_required_field] = attr

        return data

    def validate_required_field(self, raise_exception=True):
        errors = []
        for required_field in self.required_fields:
            value = getattr(self, required_field, None)
            if value is None:
                errors.append(required_field)

        if raise_exception and errors:
            raise ValueError(errors)

    @property
    def fields(self):
        """
        the fields of ZoopBase are it's __FIELDS attrs.
        it's important to be a new list (high order function)
        Returns: new list of attributes
        """
        return self.required_fields + self.non_required_fields

    @property
    def required_fields(self):
        return []

    @property
    def non_required_fields(self):
        return []


class ZoopBaseCreationSuppresed(ZoopBase):
    """
    This class represent a bare ZoopBase object which doesn't have
    to be created. It may return None on `from_dict` method.

    A instance of this class doesn't have attributes.

    This class has the attribute __FIELDS with the list of attributes it has.
    The purpose of this is to construct the dict of the object.
    """

    @classmethod
    def from_dict(cls, data):
        """
        construct a instance of this class from dict
        May return None

        Args:
            data: dict of data

        Examples:
            >>>data = None
            >>>print(**data)
            Traceback (most recent call last):
              File "<input>", line 1, in <module>
            TypeError: print() argument after ** must be a mapping, not NoneType

            >>>instance = cls.from_dict(data=None)
            instance = None

        Returns: instance initialized of cls or None
        """
        try:
            return super().from_dict(data)
        except ValueError as e:
            e.args = (f'{cls} could not be created!',)
            logger.warning(e)
            return None


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

    @property
    def required_fields(self):
        return []

    @property
    def non_required_fields(self):
        return ["id", "resource", "uri", "created_at", "updated_at", "metadata"]


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


class AddressModel(ZoopBaseCreationSuppresed):
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
                 taxpayer_id, phone_number, birthdate=None,
                 address=None, **kwargs):
        super().__init__(**kwargs)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.taxpayer_id = taxpayer_id
        self.phone_number = phone_number
        self.birthdate = birthdate

        self.address = AddressModel.from_dict_or_instance(address)

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

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


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


class VerificationChecklist(ZoopBaseCreationSuppresed):
    """
    This class and it's subclasses have attributes.

    The __FIELDS list the attributes this class
    has responsability of constructing in the serialization to dict.

    Attributes:
        postal_code_check: boolean of verification
        address_line1_check: boolean of verification
    """
    __FIELDS = ["postal_code_check", "address_line1_check"]

    def __init__(self, postal_code_check, address_line1_check,
                 **kwargs):
        super().__init__(**kwargs)

        self.postal_code_check = postal_code_check
        self.address_line1_check = address_line1_check

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

    def __init__(self, description, customer,
                 address=None, **kwargs):
        super().__init__(**kwargs)

        self.description = description
        self.customer = customer
        self.address = AddressModel.from_dict_or_instance(address)

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
