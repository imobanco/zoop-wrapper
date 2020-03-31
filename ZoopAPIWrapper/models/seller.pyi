from ZoopAPIWrapper.models.base import Address as Address, BusinessOrIndividualModel as BusinessOrIndividualModel, FinancialModel as FinancialModel, Person as Person, SocialModel as SocialModel
from typing import Any, Optional, Union, Dict

class Seller(BusinessOrIndividualModel, Person, FinancialModel, SocialModel):
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

    website: Optional[str]

    owner: Optional[Person]
    business_address: Optional[Address]
    business_name: Optional[str]
    business_phone: Optional[str]
    business_email: Optional[str]
    business_website: Optional[str]
    business_opening_date: Optional[str]
    business_description: Optional[str]
    business_facebook: Optional[str]
    business_twitter: Optional[str]
    def init_custom_fields(self, business_address=Optional[Union[Dict[str, str], Address]], owner=Optional[Union[Dict[str, str], Person]], **kwargs) -> None: ...  # type: ignore
    @classmethod
    def get_non_required_fields(cls): ...
    @classmethod
    def get_required_fields(cls): ...
    @classmethod
    def get_business_non_required_fields(cls): ...
    @classmethod
    def get_business_required_fields(cls): ...
    @classmethod
    def get_individual_non_required_fields(cls): ...
    @classmethod
    def get_individual_required_fields(cls): ...
    @property
    def full_name(self): ...
    @classmethod
    def from_dict(cls, data: Dict[str, Any], allow_empty: bool=...) -> Seller: ...
