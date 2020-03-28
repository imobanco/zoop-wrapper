from logging import Logger
from typing import Any, Optional

logger: Logger

class ZoopBase:
    __allow_empty: bool
    def __init__(self, allow_empty: bool=..., **kwargs: Any) -> None: ...
    @classmethod
    def from_dict(cls: Any, data: Any, allow_empty: bool=...) -> ZoopBase: ...
    @classmethod
    def from_dict_or_instance(cls: Any, data: Any, allow_empty: bool=...) -> ZoopBase: ...
    def to_dict(self) -> dict: ...
    def validate_fields(self, raise_exception: Optional[bool]=...) -> None: ...
    def get_validation_fields(self) -> set: ...
    def get_all_fields(self) -> set: ...
    @classmethod
    def get_fields(cls: Any) -> set: ...
    @classmethod
    def get_required_fields(cls: Any) -> set: ...
    @classmethod
    def get_non_required_fields(cls: Any) -> set: ...

class ZoopModel(ZoopBase):
    id: str
    resource: str
    uri: str
    created_at: str
    updated_at: str
    metadata: dict
    RESOURCE: str
    @classmethod
    def get_non_required_fields(cls: Any) -> set: ...

class ZoopMarketPlaceModel(ZoopModel):
    marketplace_id: str
    @classmethod
    def get_non_required_fields(cls: Any) -> set: ...

class AddressModel(ZoopBase):
    line1: str
    line2: str
    line3: str
    neighborhood: str
    city: str
    state: str
    postal_code: str
    country_code: str
    @classmethod
    def get_non_required_fields(cls: Any) -> set: ...

class OwnerModel(ZoopBase):
    address: AddressModel
    birthdate: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    taxpayer_id: str
    def __init__(self, address: Any, **kwargs: Any) -> None: ...
    @classmethod
    def get_required_fields(cls: Any) -> set: ...
    @property
    def full_name(self) -> str: ...

class SocialModel(ZoopBase):
    facebook: str
    twitter: str
    @classmethod
    def get_non_required_fields(cls: Any) -> set: ...

class FinancialModel(ZoopBase):
    status: str
    account_balance: float
    current_balance: float
    description: str
    delinquent: str
    payment_methods: Any
    default_debit: bool
    default_credit: bool
    @classmethod
    def get_non_required_fields(cls: Any) -> set: ...

class VerificationChecklist(ZoopBase):
    postal_code_check: bool
    address_line1_check: bool
    @classmethod
    def get_required_fields(cls: Any) -> set: ...

class PaymentMethod(ZoopModel):
    description: str
    customer: str
    address: AddressModel = ...
    def __init__(self, address: Any, **kwargs: Any) -> None: ...
    @classmethod
    def get_required_fields(cls: Any) -> set: ...
