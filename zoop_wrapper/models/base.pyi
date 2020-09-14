from logging import Logger
from typing import Any, Optional, Dict, Union, List

logger: Logger

class ZoopObject:
    _allow_empty: bool
    def __init__(self, allow_empty: bool = ..., **kwargs: Any) -> None: ...
    def init_custom_fields(self, **kwargs: Any) -> None: ...
    @staticmethod
    def make_data_copy_with_kwargs(
        data: Dict[str, Any], **kwargs
    ) -> Dict[str, Any]: ...
    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], allow_empty: bool = ..., **kwargs: Any
    ) -> ZoopObject: ...
    @classmethod
    def from_dict_or_instance(
        cls,
        data: Union[Dict[str, Any], ZoopObject],
        allow_empty: bool = ...,
        **kwargs: Any,
    ) -> ZoopObject: ...
    @staticmethod
    def is_value_empty(value: Any) -> bool: ...
    def to_dict(self) -> Dict[str, Any]: ...
    def validate_fields(
        self, raise_exception: Optional[bool] = ..., **kwargs: Dict[str, Any]
    ) -> None: ...
    def validate_custom_fields(self, **kwargs: Any) -> List[Any]: ...
    def get_validation_fields(self) -> set: ...
    def get_all_fields(self) -> set: ...
    def get_original_different_fields_mapping(self) -> Dict[str, str]: ...
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
    @classmethod
    def from_dict_or_instance(cls, data: Union[Dict[str, Any], ResourceModel], allow_empty: bool = ..., **kwargs: Any) -> ResourceModel: ...  # type: ignore

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
    address: Optional[Address]
    birthdate: Optional[str]
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    taxpayer_id: Optional[str]
    def validate_custom_fields(self, **kwargs) -> List[Any]: ...
    def init_custom_fields(self, address: Union[Dict[str, Any], Address], **kwargs) -> None: ...  # type: ignore
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
    def init_custom_fields(self, address: Union[Dict[str, Any], Address], **kwargs) -> None: ...  # type: ignore
    @classmethod
    def get_required_fields(cls) -> set: ...

class BusinessOrIndividualModel(MarketPlaceModel):
    BUSINESS_IDENTIFIER: str = ...
    BUSINESS_TYPE: str = ...
    INDIVIDUAL_IDENTIFIER: str = ...
    INDIVIDUAL_TYPE: str = ...
    URI: Dict[str, str] = ...

    taxpayer_id: Optional[str]
    ein: Optional[str]
    @classmethod
    def validate_identifiers(cls, taxpayer_id: str, ein: str) -> None: ...
    def get_type(self): ...
    def get_type_uri(self): ...
    def set_identifier(
        self, taxpayer_id: Optional[str] = ..., ein: Optional[str] = ...
    ) -> None: ...
    def get_validation_fields(self) -> set: ...
    def get_all_fields(self) -> set: ...
    @classmethod
    def get_business_non_required_fields(cls) -> set: ...
    @classmethod
    def get_business_required_fields(cls) -> set: ...
    @classmethod
    def get_individual_non_required_fields(cls) -> set: ...
    @classmethod
    def get_individual_required_fields(cls) -> set: ...
