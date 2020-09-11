from .base import (
    BusinessOrIndividualModel,
    Person,
    SocialModel,
    Address,
    FinancialModel,
)


class Seller(BusinessOrIndividualModel, Person, FinancialModel, SocialModel):
    """
    Represent a seller.
    https://docs.zoop.co/reference#vendedor-1

    The :attr:`RESOURCE` is used to identify this Model.
    Used to check against :attr:`.resource`!

    Attributes:
        decline_on_fail_security_code (bool): value of verification
        decline_on_fail_zipcode (bool): value of verification
        is_mobile (bool): value of verification
        mcc: ?
        merchant_code: ?
        show_profile_online: ?
        statement_descriptor: ?
        terminal_code: ?

        type (str): individual or business string

        taxpayer_id (str): Optional value
        website (str): Optional value

        business_address (:class:`.Address`): Optional value
        business_description (str): optional value
        business_email (str): optional value
        business_facebook (str): optional value
        business_name (str): optional value
        business_opening_date (str): optional value
        business_phone (str): optional value
        business_twitter (str): optional value
        business_website (str): optional value
        ein (str): optional value
        owner (:class:`.Person`): Optional value
    """

    RESOURCE = "seller"

    def validate_custom_fields(self, **kwargs):
        """
        Caso o vendedor seja :attr:`.BUSINESS_TYPE` precisamos validar os campos pelo
        :class:`.BusinessOrIndividualModel`.

        Caso o vendedor seja :attr:`.INDIVIDUAL_TYPE` precisamos validar os campos pelo
        :class:`.Person`.

        Args:
            **kwargs:
        """
        if self.get_type() == self.INDIVIDUAL_TYPE:
            return Person.validate_custom_fields(self, **kwargs)
        return []

    def init_custom_fields(self, business_address=None, owner=None, **kwargs):
        """
        If ``dynamic type`` is :attr:`.BUSINESS_TYPE` then
        initialize :attr:`owner` with :class:`.Person` and
        initialize :attr:`business_address` with :class:`.Address`.

        Else ``dynamic type`` is :attr:`.INDIVIDUAL_TYPE`! Then
        initialize ``self`` with :class:`.Person`.

        Args:
            business_address (dict or :class:`.Address`): data
            owner (dict or :class:`.Person`): data
            **kwargs: kwargs
        """
        self.set_identifier(**kwargs)

        if self.get_type() == self.BUSINESS_TYPE:
            setattr(
                self,
                "owner",
                Person.from_dict_or_instance(owner, allow_empty=True),
            )
            setattr(
                self,
                "business_address",
                Address.from_dict_or_instance(business_address, allow_empty=True),
            )
        else:
            Person.init_custom_fields(self, **kwargs)

    @classmethod
    def get_non_required_fields(cls):
        fields = set()
        return fields.union(
            BusinessOrIndividualModel.get_non_required_fields(),
            FinancialModel.get_non_required_fields(),
            {
                "decline_on_fail_security_code",
                "decline_on_fail_zipcode",
                "is_mobile",
                "show_profile_online",
                "statement_descriptor",
                "terminal_code",
                "type",
                "merchant_code",
                "mcc",
            },
        )

    @classmethod
    def get_required_fields(cls):
        fields = set()
        return fields.union(
            BusinessOrIndividualModel.get_required_fields(),
            FinancialModel.get_required_fields(),
        )

    @classmethod
    def get_business_non_required_fields(cls):
        """
        Get ``set`` of ``non required fields`` for :attr:`.BUSINESS_TYPE`

        Returns:
            ``set`` of fields
        """
        fields = cls.get_non_required_fields()
        return fields.union(
            super().get_business_non_required_fields(),
            {
                "business_description",
                "business_website",
                "business_facebook",
                "business_twitter",
                "owner",
            },
        )

    @classmethod
    def get_business_required_fields(cls):
        """
        Get ``set`` of ``required fields`` for :attr:`.BUSINESS_TYPE`

        Returns:
            ``set` `of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            super().get_business_required_fields(),
            {
                "business_address",
                "business_email",
                "business_name",
                "business_opening_date",
                "business_phone",
            },
        )

    @classmethod
    def get_individual_non_required_fields(cls):
        """
        Get ``set`` of ``non required fields`` for :attr:`.INDIVIDUAL_TYPE`

        Returns:
            ``set`` of fields
        """
        fields = cls.get_non_required_fields()
        return fields.union(
            super().get_individual_non_required_fields(),
            SocialModel.get_non_required_fields(),
            Person.get_non_required_fields(),
            {"website"},
        )

    @classmethod
    def get_individual_required_fields(cls):
        """
        Get ``set`` of ``required fields`` for :attr:`.INDIVIDUAL_TYPE`

        Returns:
            ``set`` of fields
        """
        fields = cls.get_required_fields()
        return fields.union(
            super().get_individual_required_fields(),
            SocialModel.get_required_fields(),
            Person.get_required_fields(),
        )

    @property
    def full_name(self):
        """
        Get ``full name`` for the :class:`.Seller`.

        If ``dynamic type`` is :attr:`.BUSINESS_TYPE` it will have
        the owner attribute.\n

        Else `dynamic type`` is :attr:`.INDIVIDUAL_TYPE`. So we call
        the super() which will find the method on Person class.\n

        Returns:
            string with the ``full name``
        """
        owner = getattr(self, "owner", None)
        if owner is not None:
            return owner.full_name
        return super().full_name
