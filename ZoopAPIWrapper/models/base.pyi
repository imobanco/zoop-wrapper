from ZoopAPIWrapper.utils import get_logger as get_logger
from typing import Any, Optional, Union, List

logger: Any
class ZoopBase:
    __allow_empty: bool

    def __init__(self, allow_empty: bool=..., **kwargs: Any) -> None: ...
    @classmethod
    def from_dict(cls: Any, data: dict, allow_empty: bool=...) -> ZoopBase: ...
    @classmethod
    def from_dict_or_instance(cls: Any, data: dict) -> ZoopBase: ...
    def to_dict(self) -> dict: ...
    def validate_required_fields(self, raise_exception: bool=...) -> None: ...
    @property
    def fields(self) -> List[str]: ...
    @property
    def required_fields(self) -> List[str]: ...
    @property
    def non_required_fields(self) -> List[str]: ...


class ZoopModel(ZoopBase):
    id: str
    resource: str
    uri: str
    metadata: dict
    created_at: str
    updated_at: str

    @property
    def required_fields(self) -> List[str]: ...
    @property
    def non_required_fields(self) -> List[str]: ...

class ZoopMarketPlaceModel(ZoopModel):
    marketplace_id: Any = ...
    def __init__(self, marketplace_id: Optional[Any] = ..., **kwargs: Any) -> None: ...
    @property
    def fields(self): ...

class AddressModel(ZoopBaseCreationSuppresed):
    line1: Any = ...
    line2: Any = ...
    line3: Any = ...
    neighborhood: Any = ...
    city: Any = ...
    state: Any = ...
    postal_code: Any = ...
    country_code: Any = ...
    def __init__(self, line1: Any, line2: Any, line3: Any, neighborhood: Any, city: Any, state: Any, postal_code: Any, country_code: Any, **kwargs: Any) -> None: ...
    @property
    def fields(self): ...

class OwnerModel(ZoopBase):
    first_name: Any = ...
    last_name: Any = ...
    email: Any = ...
    taxpayer_id: Any = ...
    phone_number: Any = ...
    birthdate: Any = ...
    address: Any = ...
    def __init__(self, first_name: Any, last_name: Any, email: Any, taxpayer_id: Any, phone_number: Any, birthdate: Optional[Any] = ..., address: Optional[Any] = ..., **kwargs: Any) -> None: ...
    @property
    def fields(self): ...
    @property
    def full_name(self): ...

class SocialModel(ZoopBase):
    facebook: Any = ...
    twitter: Any = ...
    def __init__(self, facebook: Optional[Any] = ..., twitter: Optional[Any] = ..., **kwargs: Any) -> None: ...
    @property
    def fields(self): ...

class FinancialModel(ZoopBase):
    status: Any = ...
    account_balance: Any = ...
    current_balance: Any = ...
    description: Any = ...
    delinquent: Any = ...
    payment_methods: Any = ...
    default_debit: Any = ...
    default_credit: Any = ...
    def __init__(self, status: Optional[Any] = ..., account_balance: Optional[Any] = ..., current_balance: Optional[Any] = ..., description: Optional[Any] = ..., delinquent: Optional[Any] = ..., payment_methods: Optional[Any] = ..., default_debit: Optional[Any] = ..., default_credit: Optional[Any] = ..., **kwargs: Any) -> None: ...
    @property
    def fields(self): ...

class VerificationChecklist(ZoopBaseCreationSuppresed):
    postal_code_check: Any = ...
    address_line1_check: Any = ...
    def __init__(self, postal_code_check: Any, address_line1_check: Any, **kwargs: Any) -> None: ...
    @property
    def fields(self): ...

class PaymentMethod(ZoopModel):
    description: Any = ...
    customer: Any = ...
    address: Any = ...
    def __init__(self, description: Any, customer: Any, address: Optional[Any] = ..., **kwargs: Any) -> None: ...
    @property
    def fields(self): ...
