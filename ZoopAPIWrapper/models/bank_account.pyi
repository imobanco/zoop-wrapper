from ZoopAPIWrapper.models.base import Address as Address, BusinessOrIndividualModel as BusinessOrIndividualModel, MarketPlaceModel as MarketPlaceModel, VerificationModel as VerificationModel
from ZoopAPIWrapper.models.seller import Seller
from typing import Any, Optional, Union, Dict

class BankAccountVerificationModel(VerificationModel):
    deposit_check: bool
    @classmethod
    def get_required_fields(cls) -> set: ...

class BankAccount(BusinessOrIndividualModel):
    RESOURCE: str = ...
    account_number: str
    bank_code: str
    holder_name: str
    routing_number: str
    address: Address
    verification_checklist: BankAccountVerificationModel
    bank_name: Optional[str]
    country_code: Optional[str]
    customer: Optional[str]
    description: Optional[str]
    debitable:  Optional[str]
    fingerprint: Optional[str]
    is_active: Optional[bool]
    is_verified: Optional[bool]
    last4_digits: Optional[str]
    phone_number: Optional[str]
    type: Optional[str]
    def __init__(self, address: Optional[Union[Dict[str, Any], Address]] = ..., verification_checklist: Optional[Dict[str, Any], BankAccountVerificationModel] = ..., **kwargs: Any) -> None: ...    @classmethod
    @classmethod
    def get_required_fields(cls) -> set: ...
    @classmethod
    def get_non_required_fields(cls) -> set: ...
    @classmethod
    def from_dict_and_seller(cls, seller: Seller, data: Dict[str, Any]) -> BankAccount: ...
