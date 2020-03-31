from ZoopAPIWrapper.models.base import (
    BusinessOrIndividualModel, Person, SocialModel, Address, FinancialModel)


class Seller(BusinessOrIndividualModel, Person,
             FinancialModel, SocialModel):
    """
    Represent a seller.
    https://docs.zoop.co/reference#vendedor-1

    This class and it's subclasses have attributes.

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        statement_descriptor: ?
        mcc: ?
        show_profile_online:
        is_mobile: bolean of verification
        decline_on_fail_security_code: bolean of verification
        decline_on_fail_zipcode: bolean of verification
        merchant_code: ?
        terminal_code: ?

        type: individual or business string

        website: Optional[str]
        taxpayer_id: Optional[str]

        ein: Optional[str]
        owner: Optional[OwnerModel]
        business_address: Optional[AddressModel]
        business_name: Optional[str]
        business_phone: Optional[str]
        business_email: Optional[str]
        business_website: Optional[str]
        business_opening_date: Optional[str]
        business_description: Optional[str]
        business_facebook: Optional[str]
        business_twitter: Optional[str]
    """
    RESOURCE = 'seller'

    def __init__(self, business_address=None, owner=None, **kwargs):
        """
        Seller init must call its superclasses init's methods individually.
        Because MRO its not trusted to Business/Individual type

        Args:
            business_address: Address instance or data
            owner: Person instance or data
            **kwargs:
        """
        # noinspection PyCallByClass
        BusinessOrIndividualModel.__init__(self, **kwargs)

        if self.get_type() == self.BUSINESS_TYPE:
            self.owner = Person.from_dict_or_instance(owner)
            self.business_address = Address\
                .from_dict_or_instance(business_address)

        elif self.get_type() == self.INDIVIDUAL_TYPE:
            Person.__init__(self, **kwargs)
            SocialModel.__init__(self, **kwargs)
        else:
            raise TypeError('Type no identified!')

        FinancialModel.__init__(self, **kwargs)

    @classmethod
    def get_non_required_fields(cls):
        """
        get set of non required fields

        Returns: set of fields
        """
        fields = set()
        return fields.union(
            BusinessOrIndividualModel.get_non_required_fields(),
            FinancialModel.get_non_required_fields(),
            {"type", "statement_descriptor", "mcc",
             "show_profile_online", "is_mobile",
             "decline_on_fail_security_code",
             "decline_on_fail_zipcode",
             "merchant_code", "terminal_code"}
        )

    @classmethod
    def get_required_fields(cls):
        """
        get set of non required fields

        Returns: set of fields
        """
        fields = set()
        return fields.union(
            BusinessOrIndividualModel.get_required_fields(),
            FinancialModel.get_required_fields()
        )

    @classmethod
    def get_business_non_required_fields(cls):
        """
        get set of non required fields for Business

        Returns: set of fields
        """
        fields = cls.get_non_required_fields()
        return fields.union(
            super().get_business_non_required_fields(),
            {'business_description', 'business_facebook',
             'business_twitter'}
        )

    @classmethod
    def get_business_required_fields(cls):
        """
        get set of required fields for Business

        Returns: set of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            super().get_business_required_fields(),
            {'business_name', 'business_phone',
             'business_email', 'business_website',
             'business_opening_date', 'owner', 'business_address'}
        )

    @classmethod
    def get_individual_non_required_fields(cls):
        """
        get set of non required fields for Individual

        Returns: set of fields
        """
        fields = cls.get_non_required_fields()
        return fields.union(
            super().get_individual_non_required_fields(),
            SocialModel.get_non_required_fields(),
            Person.get_non_required_fields(),
            {'website'}
        )

    @classmethod
    def get_individual_required_fields(cls):
        """
        get set of required fields for Individual

        Returns: set of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            super().get_individual_required_fields(),
            SocialModel.get_required_fields(),
            Person.get_required_fields()
        )

    @property
    def full_name(self):
        owner = getattr(self, 'owner', None)
        if owner is not None:
            return owner.full_name
        return super().full_name
