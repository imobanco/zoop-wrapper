import copy

from pycpfcnpj import cpf, cnpj

from ..utils import get_logger
from ..exceptions import ValidationError, FieldError


logger = get_logger("models")


class ZoopObject(object):
    """
    This class represent a bare Zoop object.

    Attributes:
        _allow_empty: boolean
    """

    def __init__(self, allow_empty=False, **kwargs):
        """
        initialize ``all fields`` from :meth:`get_all_fields` as
        ``attributes`` from ``kwargs`` on instance.

        Then call :meth:`validate_fields`.

        Args:
            allow_empty: boolean which disable validation of required fields
            **kwargs: dictionary of args
        """
        self._allow_empty = allow_empty
        self.init_custom_fields(**kwargs)

        for field_name in self.get_all_fields():
            my_value = getattr(self, field_name, None)
            if my_value is not None:
                continue

            value = kwargs.get(field_name, None)
            setattr(self, field_name, value)

        self.validate_fields(**kwargs)

    def init_custom_fields(self, **kwargs):
        """
        this method exists to set custom attributes such
        as :class:`ZoopObject` instances. Since all attributes set on
        :meth:`__init__` are ``dict's`` or ``variables``.

        Args:
            **kwargs: dictionary of args
        """
        pass

    @staticmethod
    def make_data_copy_with_kwargs(data, **kwargs):
        """
        make a new data dict from previous data dict
        with added ``kwargs``

        if ``data`` is ``None`` create a ``new empty dict``.\n

        ``data`` may be ``None`` for the cases we are explicitly calling
        with ``allow_empty=True`` on :meth:`init_custom_fields` for some
        custom :class:`ZoopObject` instance set.
        Such as::
            instance = ZoopObject()
            setattr(
                instance, 'address',
                Address.from_dict_or_instance(None, allow_empty=True)
            )

        Args:
            data: dict of data may be None
            **kwargs: dict of kwargs

        Returns:
            new dict of data
        """
        if data is None:
            _data = {}
        else:
            _data = copy.deepcopy(data)

        _data.update(kwargs)

        return _data

    @classmethod
    def from_dict(cls, data, allow_empty=False, **kwargs):
        """
        to construct a instance of this ``class`` from ``dict``

        Args:
            data: dict of data
            allow_empty: boolean
            **kwargs: kwargs
            data: dict of data may be None
            allow_empty: boolean
            **kwargs: kwargs

        Returns:
            instance initialized of cls
        """
        _data = cls.make_data_copy_with_kwargs(data, allow_empty=allow_empty, **kwargs)
        return cls(**_data)

    @classmethod
    def from_dict_or_instance(cls, data, **kwargs):
        """
        check if ``data`` is already a :class:`ZoopObject` or
        ``subclass``.\n

        If not call :meth:`from_dict`.

        Args:
            data: dict of data or instance
            **kwargs: kwargs

        Returns:
            instance initialized of ``cls``
        """
        if isinstance(data, cls):
            return data
        else:
            return cls.from_dict(data, **kwargs)

    @staticmethod
    def is_value_empty(value):
        """
        Verify if ``value`` passed is considered ``empty``!

        ``value`` may be ``None``.
        As we set on :meth:`__init__`::
            value = kwargs.get(field_name, None)

        ``value`` may be ``{}`` if it was a :class:`ZoopObject`
        with allow_empty! \n

        ``value`` may be ``[{}]`` if it was a ``list`` of
        :class:`ZoopObject`'s with ``allow_empty``!!

        Args:
            value: Value to be verified

        Returns:
            boolean
        """
        return value is None or value == {} or value == [{}]

    def to_dict(self):
        """
        serialize ``self`` to dict

        Returns:
            dict of instance
        """
        data = {}
        for field in self.get_all_fields():
            value = getattr(self, field)

            if isinstance(value, list):
                """our value is a list!
                It may be a list of ZoopObject's.
                Let's try to get its serialized value!"""
                try:
                    value = [item.to_dict() for item in value]
                except AttributeError:
                    pass
            else:
                try:
                    """our value is not a list!
                    It may be a ZoopObject instance.
                    Let's try to get its serialized value!"""
                    value = value.to_dict()
                except AttributeError:
                    pass

            if self.is_value_empty(value):
                continue

            data[field] = value

        return data

    def validate_fields(self, raise_exception=True, **kwargs):
        """
        Validate fields returned from :meth:`get_validation_fields`.\n

        if :attr:`_allow_empty` is ``True`` don't validate!

        Args:
            raise_exception: boolean to raise or not exception

        Raises:
            :class:`.ValidationError`: if there's some ``required field`` missing and ``raise_exception==True``

        """
        if self._allow_empty:
            return

        errors = []
        for validation_field in self.get_validation_fields():
            value = getattr(self, validation_field, None)
            if value is None:
                errors.append(FieldError(validation_field, "missing required field"))

        if errors and raise_exception:
            raise ValidationError(self, errors)

    def get_validation_fields(self):
        """
        Get ``validation fields`` for instance.\n

        This is necessary for classes/instances with
        different fields based on type.\n

        Such as :class:`.Seller`, :class:`.BankAccount`,
        :class:`.BillingConfiguration` and :class:`.Token`.\n

        Defaults to :meth:`get_required_fields`.

        Returns:
            ``set`` of fields to be used on validation
        """
        return self.get_required_fields()

    def get_all_fields(self):
        """
        get ``all fields`` for instance.\n

        This is necessary for classes/instances with
        different fields based on type.\n

        Such as :class:`.Seller`, :class:`.BankAccount`,
        :class:`.BillingConfiguration` and :class:`.Token`.\n

        Defaults to :meth:`get_fields`.

        Returns:
            ``set`` of all fields
        """
        return self.get_fields()

    @classmethod
    def get_fields(cls):
        """
        get ``set`` of ``all fields``

        Returns:
            ``set`` of fields
        """
        required_fields = cls.get_required_fields()
        non_required_fields = cls.get_non_required_fields()
        return required_fields.union(non_required_fields)

    @classmethod
    def get_required_fields(cls):
        """
        get ``set`` of ``required fields``

        Returns:
            ``set`` of fields
        """
        return set()

    @classmethod
    def get_non_required_fields(cls):
        """
        get ``set`` of ``non required fields``

        Returns:
            ``set`` of fields
        """
        return set()


class ResourceModel(ZoopObject):
    """
    Represents a Model that is a ``resource``.

    Attributes:
        id: identifier string
        resource: type string
        uri: uri string
        created_at: date of creation
        updated_at: date of update
        metadata: dict with metadata
    """

    RESOURCE = None

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {"id", "resource", "uri", "created_at", "updated_at", "metadata"}
        )


class MarketPlaceModel(ResourceModel):
    """
    This class represents a :class:`.ResourceModel` which belongs
    to some ``marketplace`` from ``Zoop``.

    Attributes:
        marketplace_id: identifier string
    """

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union({"marketplace_id"})


class Address(ZoopObject):
    """
    Represents a physical ``address``.

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
        fields = super().get_non_required_fields()
        return fields.union(
            {
                "line1",
                "line2",
                "line3",
                "neighborhood",
                "city",
                "state",
                "postal_code",
                "country_code",
            }
        )


class Person(ZoopObject):
    """
    Represents a ``person``.

    Attributes:
        address: Address model
        birthdate: birthdate
        email: email
        first_name: first name
        last_name: last name
        phone_number: phone number
        taxpayer_id: cpf válido
    """

    def validate_fields(self, raise_exception=True, **kwargs):
        """
        O :attr:`taxpayer_id` precisa ser um CPF válido. Então verificamos isso.

        Args:
            raise_exception: Quando algum campo está faltando ou CPF é inválido
            **kwargs:
        """
        super().validate_fields()

        if self._allow_empty:
            return

        if not cpf.validate(self.taxpayer_id):
            raise ValidationError(
                self, FieldError("taxpayer_id", "taxpayer_id inválido!")
            )

    def init_custom_fields(self, address=None, **kwargs):
        """
        Initialize :attr:`address` with :class:`.Address`

        Args:
            address: dict of data or :class:`.Address`
            **kwargs:
        """
        setattr(
            self, "address", Address.from_dict_or_instance(address, allow_empty=True)
        )

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union(
            {
                "first_name",
                "last_name",
                "email",
                "taxpayer_id",
                "phone_number",
                "address",
            }
        )

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union({"birthdate"})

    @property
    def full_name(self):
        """
        get ``full name`` of the person

        Returns:
            string with the ``full name``
        """
        return f"{self.first_name} {self.last_name}"


class SocialModel(ZoopObject):
    """
    Have social sites uri's

    Attributes:
        facebook: facebook profile url?
        twitter: twitter profile url?
    """

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union({"facebook", "twitter"})


class FinancialModel(ZoopObject):
    """
    Have financial attributes.

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

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {
                "status",
                "account_balance",
                "current_balance",
                "description",
                "delinquent",
                "payment_methods",
                "default_debit",
                "default_credit",
            }
        )


class VerificationModel(ZoopObject):
    """
    Have some verification attributes.

    Attributes:
        postal_code_check: boolean of verification
        address_line1_check: boolean of verification
    """

    @classmethod
    def get_required_fields(cls):
        fields = super().get_required_fields()
        return fields.union({"postal_code_check", "address_line1_check"})


class PaymentMethod(ResourceModel):
    """
    Have some payment method attributes

    Attributes:
        description: text description
        customer: uuid id
        address: Address Model
    """

    def init_custom_fields(self, address=None, **kwargs):
        """
        initialize :attr:`address` with :class:`.Address`

        Args:
            address: dict of data or :class:`.Address`
            **kwargs: dic of kwargs
        """
        setattr(
            self, "address", Address.from_dict_or_instance(address, allow_empty=True)
        )

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union({"description", "customer", "address"})


class BusinessOrIndividualModel(MarketPlaceModel):
    """
    Represents a ``Business`` Or ``Individual`` Model\n

    It has ``dynamic types``!\n

    Can be ``Business`` or ``Individual``.

    Attributes:
        taxpayer_id: cpf válido para ``type`` :attr:`INDIVIDUAL_TYPE`
        ein: cnpj para ``type`` :attr:`BUSINESS_TYPE`
    """

    BUSINESS_IDENTIFIER = "ein"
    BUSINESS_TYPE = "business"

    INDIVIDUAL_IDENTIFIER = "taxpayer_id"
    INDIVIDUAL_TYPE = "individual"

    URI = {BUSINESS_TYPE: "businesses", INDIVIDUAL_TYPE: "individuals"}

    def init_custom_fields(self, taxpayer_id=None, ein=None, **kwargs):
        """
        call :meth:`set_identifier`.

        Args:
            taxpayer_id: cpf value
            ein: cnpj value
            **kwargs: dict of kwargs
        """
        self.set_identifier(taxpayer_id, ein)

    @classmethod
    def validate_identifiers(cls, taxpayer_id, ein):
        """
        valida tupla de valores de identificação

        Raises:
            :class`.ValidationError`: quando é passado os dois, ou nenhum, ou quando o identificador passado é inválido
        """
        if (taxpayer_id is not None and ein is not None) or (
            taxpayer_id is None and ein is None
        ):
            raise ValidationError(
                cls,
                FieldError(
                    f"{BusinessOrIndividualModel.INDIVIDUAL_IDENTIFIER} "
                    f"ou {BusinessOrIndividualModel.BUSINESS_IDENTIFIER}",
                    "identificadores faltando!",
                ),
            )
        elif taxpayer_id is not None and not cpf.validate(taxpayer_id):
            raise ValidationError(
                cls, FieldError("taxpayer_id", "taxpayer_id inválido!")
            )
        elif ein is not None and not cnpj.validate(ein):
            raise ValidationError(cls, FieldError("ein", "ein inválido!"))

    def get_type(self):
        """
        get the ``dynamic type`` from instance

        Returns:
            :attr:`BUSINESS_TYPE` or :attr:`INDIVIDUAL_TYPE`
        """
        individual_identifier = getattr(
            self, BusinessOrIndividualModel.INDIVIDUAL_IDENTIFIER, None
        )
        business_identifier = getattr(
            self, BusinessOrIndividualModel.BUSINESS_IDENTIFIER, None
        )

        BusinessOrIndividualModel.validate_identifiers(
            individual_identifier, business_identifier
        )

        if individual_identifier:
            return BusinessOrIndividualModel.INDIVIDUAL_TYPE
        else:
            return BusinessOrIndividualModel.BUSINESS_TYPE

    def get_type_uri(self):
        """
        get the ``dynamic type uri`` for instance based on :meth:`get_type`

        Returns:
            uri string for type from :attr:`URI`
        """
        return self.URI.get(self.get_type())

    def set_identifier(self, taxpayer_id=None, ein=None, **kwargs):
        """
        set :attr:`taxpayer_id` or :attr:`ein` identifier.
        Exactly one of then have to be not None.\n

        ``kwargs`` are there to be called from :meth:`.Seller.init_custom_fields`
        and :meth:`.BankAccount.init_custom_fields` without getting
        ``taxpayer_id`` or ``ein`` variables.

        Args:
            taxpayer_id: cpf
            ein: cnpj
            **kwargs: kwarg
        """
        BusinessOrIndividualModel.validate_identifiers(taxpayer_id, ein)

        if taxpayer_id:
            setattr(self, BusinessOrIndividualModel.INDIVIDUAL_IDENTIFIER, taxpayer_id)
        else:
            setattr(self, BusinessOrIndividualModel.BUSINESS_IDENTIFIER, ein)

    def get_validation_fields(self):
        """
        Get ``validation fields`` for instance.

        if ``type`` is :attr:`BUSINESS_TYPE` then call
        :meth:`get_business_required_fields`

        else ``type`` is :attr:`INDIVIDUAL_TYPE`! then call
        :meth:`get_individual_required_fields`

        Returns:
            ``set`` of fields to be used on validation
        """
        if self.get_type() == self.BUSINESS_TYPE:
            return self.get_business_required_fields()
        else:
            return self.get_individual_required_fields()

    def get_all_fields(self):
        """
        get ``all fields`` for instance.

        if ``type`` is :attr:`BUSINESS_TYPE` then call
        :meth:`get_business_required_fields` and
        :meth:`get_business_non_required_fields`

        else ``type`` is :attr:`INDIVIDUAL_TYPE`! then call
        :meth:`get_individual_required_fields` and
        :meth:`get_individual_non_required_fields`

        Returns:
            ``set`` of all fields
        """
        fields = set()
        if self.get_type() == self.BUSINESS_TYPE:
            return fields.union(
                self.get_business_non_required_fields(),
                self.get_business_required_fields(),
            )
        else:
            return fields.union(
                self.get_individual_non_required_fields(),
                self.get_individual_required_fields(),
            )

    @classmethod
    def get_business_non_required_fields(cls):
        """
        get ``set`` of ``non required fields`` for
        :attr:`BUSINESS_TYPE`.

        Returns:
            ``set`` of fields
        """
        return cls.get_non_required_fields()

    @classmethod
    def get_business_required_fields(cls):
        """
        get ``set`` of ``required fields`` for
        :attr:`BUSINESS_TYPE`

        Returns:
            ``set`` of fields
        """
        fields = cls.get_required_fields()
        return fields.union({"ein"})

    @classmethod
    def get_individual_non_required_fields(cls):
        """
        get ``set`` of ``non required fields`` for
        :attr:`INDIVIDUAL_TYPE`

        Returns:
            ``set`` of fields
        """
        return cls.get_non_required_fields()

    @classmethod
    def get_individual_required_fields(cls):
        """
        get ``set`` of ``required fields`` for
        :attr:`INDIVIDUAL_TYPE`

        Returns:
            ``set`` of fields
        """
        fields = cls.get_required_fields()
        return fields.union({"taxpayer_id"})
