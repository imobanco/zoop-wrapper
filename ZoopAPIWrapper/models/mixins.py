class BusinessOrIndividualMixin:
    """
    BusinessOrIndividualMixin

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

    def get_type(self):
        """
        get the type from instance

        Raises:
            TypeError: when it's passed both identifiers or none

        Returns: BUSINESS_TYPE or INDIVIDUAL_TYPE
        """
        has_individual_identifier = getattr(self, self.INDIVIDUAL_IDENTIFIER, False)
        has_business_identifier = getattr(self, self.BUSINESS_IDENTIFIER, False)

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

    def set_identifier(self, taxpayer_id=None, ein=None):
        if ((taxpayer_id is not None and ein is not None) or
                (taxpayer_id is None and ein is None)):
            raise TypeError(f'Identifier error! '
                            f'Must be either "{self.INDIVIDUAL_IDENTIFIER}" or '
                            f'"{self.BUSINESS_IDENTIFIER}"')
        elif taxpayer_id:
            setattr(self, self.INDIVIDUAL_IDENTIFIER, taxpayer_id)
        else:
            setattr(self, self.BUSINESS_IDENTIFIER, ein)
