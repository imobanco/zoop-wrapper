from ZoopAPIWrapper.models.base import (
    ZoopMarketPlaceModel, OwnerModel, SocialModel, AddressModel, FinancialModel)
from ZoopAPIWrapper.models.mixins import (
    BusinessOrIndividualMixin)


class Seller(ZoopMarketPlaceModel, FinancialModel,
             SocialModel, OwnerModel,
             BusinessOrIndividualMixin):
    """
    Represent a seller.
    https://docs.zoop.co/reference#vendedor-1

    This class and it's subclasses have attributes.

    The RESOURCE attribute of this class is used to identify this Model.
    Remember the resource on ZoopModel? BAM!

    Attributes:
        type: individual or business string
        statement_descriptor: ?
        mcc: ?
        show_profile_online:
        is_mobile: bolean of verification
        decline_on_fail_security_code: bolean of verification
        decline_on_fail_zipcode: bolean of verification
        merchant_code: ?
        terminal_code: ?

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

    def __init__(self, taxpayer_id=None, ein=None,
                 business_address=None, owner=None, **kwargs):
        self.set_identifier(taxpayer_id, ein)

        if self.get_type() == self.BUSINESS_TYPE:
            self.owner = OwnerModel.from_dict_or_instance(owner)
            self.business_address = AddressModel.from_dict_or_instance(business_address)

            ZoopMarketPlaceModel.__init__(self, **kwargs)
            FinancialModel.__init__(self, **kwargs)

        elif self.get_type() == self.INDIVIDUAL_TYPE:
            super().__init__(**kwargs)
        else:
            raise TypeError('Type no identified!')

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
    def get_non_required_fields(cls):
        """
        set of non required fields

        Returns: set of fields
        """
        fields = set()
        return fields.union(
            ZoopMarketPlaceModel.get_non_required_fields(),
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
        set of non required fields

        Returns: set of fields
        """
        fields = set()
        return fields.union(
            ZoopMarketPlaceModel.get_required_fields(),
            FinancialModel.get_required_fields()
        )

    @classmethod
    def get_individual_non_required_fields(cls):
        fields = set()
        fields = fields.union(
            cls.get_non_required_fields(),
            SocialModel.get_non_required_fields(),
            OwnerModel.get_non_required_fields()
        )
        return fields.union(
            {'website'}
        )

    @classmethod
    def get_individual_required_fields(cls):
        fields = set()
        return fields.union(
            SocialModel.get_required_fields(),
            OwnerModel.get_required_fields(),
            {'taxpayer_id'}
        )

    @classmethod
    def get_business_non_required_fields(cls):
        fields = set()
        return fields.union(
            cls.get_non_required_fields(),
            {'business_description', 'business_facebook',
             'business_twitter'}
        )

    @classmethod
    def get_business_required_fields(cls):
        fields = set()
        return fields.union(
            cls.get_required_fields(),
            {'ein', 'business_name', 'business_phone',
             'business_email', 'business_website',
             'business_opening_date', 'owner', 'business_address'}
        )

    @property
    def full_name(self):
        owner = getattr(self, 'owner', None)
        if owner is not None:
            return owner.full_name
        return super().full_name
