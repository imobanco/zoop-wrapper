from logging import Logger
from typing import Any, Optional, Dict, Union

logger: Logger

class ZoopObject:
    __allow_empty: bool
    def __init__(self, allow_empty: bool=..., **kwargs: Any) -> None: ...
    @classmethod
    def from_dict(cls, data: Dict[str, Any], allow_empty: bool=...) -> ZoopObject: ...
    @classmethod
    def from_dict_or_instance(cls, data: Union[Dict[str, Any], ZoopObject], allow_empty: bool=...) -> ZoopObject: ...
    def to_dict(self) -> Dict[str, Any]: ...
    def validate_fields(self, raise_exception: Optional[bool]=...) -> None: ...
    def get_validation_fields(self) -> set: ...
    def get_all_fields(self) -> set: ...
    @classmethod
    def get_fields(cls) -> set: ...
    @classmethod
    def get_required_fields(cls) -> set: ...
    @classmethod
    def get_non_required_fields(cls) -> set: ...

class ResourceModel(ZoopObject):
    id: str
    resource: str
    uri: str
    created_at: str
    updated_at: str
    metadata: Dict[str, Any]
    RESOURCE: str
    @classmethod
    def get_non_required_fields(cls) -> set: ...

class MarketPlaceModel(ResourceModel):
    marketplace_id: str
    @classmethod
    def get_non_required_fields(cls) -> set: ...

class Address(ZoopObject):
    line1: str
    line2: str
    line3: str
    neighborhood: str
    city: str
    state: str
    postal_code: str
    country_code: str
    @classmethod
    def get_non_required_fields(cls) -> set: ...

class Person(ZoopObject):
    address: Address
    birthdate: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    taxpayer_id: str
    def __init__(self, address: Union[Dict[str, Any], Address], **kwargs: Any) -> None: ...
    @classmethod
    def get_required_fields(cls) -> set: ...
    @property
    def full_name(self) -> str: ...

class SocialModel(ZoopObject):
    facebook: str
    twitter: str
    @classmethod
    def get_non_required_fields(cls) -> set: ...

class FinancialModel(ZoopObject):
    status: str
    account_balance: float
    current_balance: float
    description: str
    delinquent: str
    payment_methods: Any
    default_debit: bool
    default_credit: bool
    @classmethod
    def get_non_required_fields(cls) -> set: ...

class VerificationModel(ZoopObject):
    postal_code_check: bool
    address_line1_check: bool
    @classmethod
    def get_required_fields(cls) -> set: ...

class PaymentMethod(ResourceModel):
    description: str
    customer: str
    address: Address = ...
    def __init__(self, address: Union[Dict[str, Any], Address], **kwargs: Any) -> None: ...
    @classmethod
    def get_required_fields(cls) -> set: ...
