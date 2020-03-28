from ZoopAPIWrapper.models.base import AddressModel as AddressModel, FinancialModel as FinancialModel, OwnerModel as OwnerModel, SocialModel as SocialModel, ZoopMarketPlaceModel as ZoopMarketPlaceModel
from ZoopAPIWrapper.models.mixins import BusinessOrIndividualMixin as BusinessOrIndividualMixin
from typing import Any, Optional


class Seller(ZoopMarketPlaceModel, FinancialModel, SocialModel, OwnerModel, BusinessOrIndividualMixin):
    RESOURCE: str = ...

    type: str

    statement_descriptor: Optional[Any]
    mcc: Optional[Any]
    show_profile_online: Optional[bool]
    is_mobile: Optional[bool]
    decline_on_fail_security_code: Optional[bool]
    decline_on_fail_zipcode: Optional[bool]
    merchant_code: Optional[Any]
    terminal_code: Optional[Any]

    taxpayer_id: Optional[str]
    address: Optional[AddressModel]
    birthdate: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    taxpayer_id: Optional[str]
    website: Optional[str]
    facebook: Optional[str]
    twitter: Optional[str]

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

    def __init__(self, taxpayer_id: Optional[Any] = ..., ein: Optional[Any] = ..., business_address: Optional[Any] = ..., owner: Optional[Any] = ..., **kwargs: Any) -> None: ...
    def get_validation_fields(self) -> set: ...
    def get_all_fields(self) -> set: ...
    @classmethod
    def get_non_required_fields(cls) -> set: ...
    @classmethod
    def get_required_fields(cls) -> set: ...
    @classmethod
    def get_individual_non_required_fields(cls) -> set: ...
    @classmethod
    def get_individual_required_fields(cls) -> set: ...
    @classmethod
    def get_business_non_required_fields(cls) -> set: ...
    @classmethod
    def get_business_required_fields(cls) -> set: ...
    @property
    def full_name(self) -> str: ...
