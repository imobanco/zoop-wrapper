from ZoopAPIWrapper.utils import classproperty


class BusinessOrIndividualMixin:
    BUSINESS_IDENTIFIER = 'ein'
    INDIVIDUAL_IDENTIFIER = 'taxpayer_id'

    # noinspection PyMethodParameters
    @classproperty
    def business_class(cls):
        raise NotImplementedError()

    # noinspection PyMethodParameters
    @classproperty
    def individual_class(cls):
        raise NotImplementedError()

    @classmethod
    def __extract_identifier(cls, data):
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
    def get_class(cls, data):
        identifier_type = cls.__extract_identifier(data)

        if identifier_type == cls.INDIVIDUAL_IDENTIFIER:
            return cls.individual_class
        elif identifier_type == cls.BUSINESS_IDENTIFIER:
            return cls.business_class
        else:
            raise ValueError('costumer_identifier type not identified')
