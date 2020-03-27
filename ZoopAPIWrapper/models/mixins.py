from ZoopAPIWrapper.utils import classproperty


class BusinessOrIndividualMixin:
    """
    BusinessOrIndividualMixin

    Attributes:
        BUSINESS_IDENTIFIER: ein/cnpj
        INDIVIDUAL_IDENTIFIER: taxpayer_id/cpf
    """
    BUSINESS_IDENTIFIER = 'ein'
    INDIVIDUAL_IDENTIFIER = 'taxpayer_id'

    # noinspection PyMethodParameters
    @classproperty
    def business_class(cls):
        """
        getter for business class
        Raises:
             NotImplementedError: it's a abstract method
        """
        raise NotImplementedError()

    # noinspection PyMethodParameters
    @classproperty
    def individual_class(cls):
        """
        getter for business class
        Raises:
             NotImplementedError: it's a abstract method
        """
        raise NotImplementedError()

    @classmethod
    def __extract_identifier(cls, data: dict):
        """
        extract a identifier type from data.
        Args:
            data: dict of data

        Raises:
            TypeError: when it's passed both identifiers or none

        Returns: BUSINESS_IDENTIFIER or INDIVIDUAL_IDENTIFIER
        """
        has_individual_identifier = data.get(cls.INDIVIDUAL_IDENTIFIER, False)
        has_business_identifier = data.get(cls.BUSINESS_IDENTIFIER, False)

        if ((not has_business_identifier and not has_individual_identifier) or
                (has_business_identifier and has_individual_identifier)):
            raise TypeError(f'missing identifier. '
                            f'Must be either "{cls.INDIVIDUAL_IDENTIFIER}" or '
                            f'"{cls.BUSINESS_IDENTIFIER}"')
        elif has_individual_identifier:
            identifier_type = cls.INDIVIDUAL_IDENTIFIER
        else:
            identifier_type = cls.BUSINESS_IDENTIFIER

        return identifier_type

    @classmethod
    def get_class(cls, data: dict):
        """
        get a class for this data.
        Args:
            data: dict of data

        Raises:
            TypeError: raised from __extract_identifier
            ValueError: Its not supposed to raise this error. WTF!?!?!?

        Returns: individual_class or business_class
        """
        identifier_type = cls.__extract_identifier(data)

        if identifier_type == cls.INDIVIDUAL_IDENTIFIER:
            return cls.individual_class
        elif identifier_type == cls.BUSINESS_IDENTIFIER:
            return cls.business_class
        else:
            raise ValueError('costumer_identifier type not identified')

    @classmethod
    def from_dict(cls, data):
        """
        construct a Individual or Business depending on BusinessOrIndividualMixin.
        Factory pattern

        Args:
            data: dict of data

        Returns: instance initialized of cls
        """
        klass = cls.get_class(data)
        return klass.from_dict(data)
