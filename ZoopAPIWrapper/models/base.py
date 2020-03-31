from ZoopAPIWrapper.utils import get_logger
from ZoopAPIWrapper.exceptions import ValidationError


logger = get_logger('models')


class ZoopObject(object):
    """
    This class represent a bare Zoop object.

    Attributes:
        __allow_empty: boolean
    """

    def __init__(self, allow_empty=False, **kwargs):
        """
        initialize all fields from get_fields method as
        attributes from kwargs on instance.

        Then validates fields.

        Args:
            allow_empty: boolean which disable validation of required fields
            **kwargs: dictionary of args
        """

        self.init_custom_fields(**kwargs)

        for field_name in self.get_all_fields():
            my_value = getattr(self, field_name, None)
            if my_value is not None:
                continue

            value = kwargs.get(field_name, None)
            setattr(self, field_name, value)

        self.__allow_empty = allow_empty

        self.validate_fields()

    def init_custom_fields(self, **kwargs):
        pass

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
            allow_empty: boolean

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
        for field in self.get_all_fields():
            try:
                """our attr may be a ZoopBase instance.
                Let's try to get its serialized value!"""
                attr = getattr(self, field).to_dict()
            except AttributeError:
                """our attr doesn't have to_dict() method.
                Oh snap! It's not a ZoopBase instance!"""
                attr = getattr(self, field)

            if attr is not None and attr != {}:
                data[field] = attr

        return data

    def validate_fields(self, raise_exception=None):
        """
        Validate fields returned from method
        get_validation_fields.

        Args:
            raise_exception: boolean to raise or not exception

        Raises:
            ValidationError: if there's some required_field missing
            and __allow_empty is false and raise_exception is true

        """
        errors = []
        for validation_field in self.get_validation_fields():
            value = getattr(self, validation_field, None)
            if value is None:
                errors.append(validation_field)

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

    def get_validation_fields(self):
        """
        Get validation fields for instance.
        This is necessary for classes/instances with
        different fields based on type.
        Such as Seller and BankAccount.

        Defaults to get_required_fields.

        Returns: set of fields to validate
        """
        return self.get_required_fields()

    def get_all_fields(self):
        """
        get all fields for instance.
        This is necessary for classes/instances with
        different fields based on type.
        Such as Seller and BankAccount.

        Defaults to get_fields.

        Returns: set of all fields
        """
        return self.get_fields()

    @classmethod
    def get_fields(cls):
        """
        get set of all fields

        Returns: set of fields
        """
        required_fields = cls.get_required_fields()
        non_required_fields = cls.get_non_required_fields()
        return required_fields.union(non_required_fields)

    @classmethod
    def get_required_fields(cls):
        """
        get set of required fields

        Returns: set of fields
        """
        return set()

    @classmethod
    def get_non_required_fields(cls):
        """
        get set of non required fields

        Returns: set of fields
        """
        return set()


class ResourceModel(ZoopObject):
    """
    Represents a Model that is a resource.

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
        """
        get set of non required fields

        Returns: set of fields
        """
        fields = super().get_non_required_fields()
        return fields.union(
            {"id", "resource", "uri", "created_at", "updated_at", "metadata"}
        )


class MarketPlaceModel(ResourceModel):
    """
    This class represents a Model which belongs
    to the marketplace from Zoop.

    Attributes:
        marketplace_id: identifier string
    """

    @classmethod
    def get_non_required_fields(cls):
        """
        get set of non required fields

        Returns: set of fields
        """
        fields = super().get_non_required_fields()
        return fields.union(
            {'marketplace_id'}
        )


class Address(ZoopObject):
    """
    Represents a physical address.

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
        get set of non required fields

        Returns: set of fields
        """
        fields = super().get_non_required_fields()
        return fields.union(
            {"line1", "line2", "line3",
             "neighborhood", "city", "state",
             "postal_code", "country_code"}
        )


class Person(ZoopObject):
    """
    Represents a person.

    Attributes:
        address: Address model
        birthdate: birthdate
        email: email
        first_name: first name
        last_name: last name
        phone_number: phone number
        taxpayer_id: cpf
    """

    def init_custom_fields(self, address, **kwargs):
        setattr(self, 'address',
                Address.from_dict_or_instance(address, allow_empty=True))

    @classmethod
    def get_required_fields(cls):
        """
        get set of required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {"first_name", "last_name", "email",
             "taxpayer_id", "phone_number",
             "birthdate", "address"}
        )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class SocialModel(ZoopObject):
    """
    Have social sites uri's

    Attributes:
        facebook: facebook profile url?
        twitter: twitter profile url?
    """

    @classmethod
    def get_non_required_fields(cls):
        """
        get set of non required fields

        Returns: set of fields
        """
        fields = super().get_non_required_fields()
        return fields.union(
            {"facebook", "twitter"}
        )


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
        """
        get set of non required fields

        Returns: set of fields
        """
        fields = super().get_non_required_fields()
        return fields.union(
            {'status', 'account_balance', 'current_balance',
             'description', 'delinquent', 'payment_methods',
             'default_debit', 'default_credit'}
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
        """
        get set of required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {"postal_code_check", "address_line1_check"}
        )


class PaymentMethod(ResourceModel):
    """
    Have some payment method attributes

    Attributes:
        description: text description
        customer: uuid id
        address: Address Model
    """

    def init_custom_fields(self, address, **kwargs):
        setattr(
            self, 'address',
            Address.from_dict_or_instance(address, allow_empty=True))

    @classmethod
    def get_required_fields(cls):
        """
        get set of required fields

        Returns: set of fields
        """
        fields = super().get_required_fields()
        return fields.union(
            {'customer', 'address'}
        )

    @classmethod
    def get_non_required_fields(cls):
        fields = super().get_non_required_fields()
        return fields.union(
            {'description'}
        )


class BusinessOrIndividualModel(MarketPlaceModel):
    """
    BusinessOrIndividualModel

    Attributes:
        BUSINESS_IDENTIFIER: 'ein'
        BUSINESS_TYPE: 'business'

        INDIVIDUAL_IDENTIFIER: 'taxpayer_id'
        INDIVIDUAL_TYPE: 'individual'

        URI: dict with uris for individuals and business
    """
    BUSINESS_IDENTIFIER = 'ein'
    BUSINESS_TYPE = 'business'

    INDIVIDUAL_IDENTIFIER = 'taxpayer_id'
    INDIVIDUAL_TYPE = 'individual'

    URI = {
        BUSINESS_TYPE: 'business',
        INDIVIDUAL_TYPE: 'individuals'
    }

    def init_custom_fields(self, taxpayer_id=None, ein=None, **kwargs):
        self.set_identifier(taxpayer_id, ein)

    def get_type(self):
        """
        get the type from instance

        Raises:
            TypeError: when it's passed both identifiers or none

        Returns: BUSINESS_TYPE or INDIVIDUAL_TYPE
        """
        has_individual_identifier = getattr(
            self, self.INDIVIDUAL_IDENTIFIER, False)
        has_business_identifier = getattr(
            self, self.BUSINESS_IDENTIFIER, False)

        if ((not has_business_identifier and not has_individual_identifier) or
                (has_business_identifier and has_individual_identifier)):
            raise TypeError(f'Identifier error! '
                            f'Must be either "{self.INDIVIDUAL_IDENTIFIER}" or '
                            f'"{self.BUSINESS_IDENTIFIER}"')
        elif has_individual_identifier:
            return self.INDIVIDUAL_TYPE
        else:
            return self.BUSINESS_TYPE

    def get_type_uri(self):
        return self.URI.get(self.get_type())

    def set_identifier(self, taxpayer_id=None, ein=None, **kwargs):
        if ((taxpayer_id is not None and ein is not None) or
                (taxpayer_id is None and ein is None)):
            raise TypeError(f'Identifier error! '
                            f'Must be either "{self.INDIVIDUAL_IDENTIFIER}" or '
                            f'"{self.BUSINESS_IDENTIFIER}"')
        elif taxpayer_id:
            setattr(self, self.INDIVIDUAL_IDENTIFIER, taxpayer_id)
        else:
            setattr(self, self.BUSINESS_IDENTIFIER, ein)

    def get_validation_fields(self):
        if self.get_type() == self.BUSINESS_TYPE:
            return self.get_business_required_fields()
        elif self.get_type() == self.INDIVIDUAL_TYPE:
            return self.get_individual_required_fields()
        else:
            raise TypeError('Type no identified!')

    def get_all_fields(self):
        fields = set()
        if self.get_type() == self.BUSINESS_TYPE:
            return fields.union(
                self.get_business_non_required_fields(),
                self.get_business_required_fields()
            )
        elif self.get_type() == self.INDIVIDUAL_TYPE:
            return fields.union(
                self.get_individual_non_required_fields(),
                self.get_individual_required_fields()
            )
        else:
            raise TypeError('Type no identified!')

    @classmethod
    def get_business_non_required_fields(cls):
        """
        get set of non required fields for Business

        Returns: set of fields
        """
        return cls.get_non_required_fields()

    @classmethod
    def get_business_required_fields(cls):
        """
        get set of required fields for Business

        Returns: set of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            {'ein'}
        )

    @classmethod
    def get_individual_non_required_fields(cls):
        """
        get set of non required fields for Individual

        Returns: set of fields
        """
        return cls.get_non_required_fields()

    @classmethod
    def get_individual_required_fields(cls):
        """
        get set of required fields for Individual

        Returns: set of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            {'taxpayer_id'}
        )
